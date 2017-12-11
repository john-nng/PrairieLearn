
# This program is the glue between python-runner JavaScript code and Python code
#
# It will enter an infinite loop waiting for input. For each input, it
# will load a single Python file and call one top-level function in
# it, passing a list of arguments and returning the entire return
# value of the function.
#
# It is intended that this process will be terminated by sending
# SIGTERM (or SIGKILL if it's stuck).
#
# Input is formatted as JSON on STDIN
# Output is formatted as JSON on file descriptor 3
# Anything written to STDOUT or STDERR will be captured and logged, but it has no meaning
# Errors are signaled by exiting with non-zero exit code
# Exceptions are not caught and so will trigger a process exit with non-zero exit code (signaling an error)

import sys, os, json, importlib, copy, base64, io, matplotlib
matplotlib.use('PDF')

saved_path = copy.copy(sys.path)

# file descriptor 3 is for output data
with open(3, 'w', encoding='utf-8') as outf:

    # Infinite loop where we wait for an input command, do it, and
    # return the results. The caller should terminate us with a
    # SIGTERM.
    while True:

        # wait for a single line of input
        json_inp = sys.stdin.readline()
        # unpack the input line as JSON
        inp = json.loads(json_inp)

        # get the contents of the JSON input
        file = inp['file']
        fcn = inp['fcn']
        args = inp['args']
        cwd = inp['cwd']
        paths = inp['paths']

        original_data_str = str(args[-1])

        # reset and then set up the path
        sys.path = copy.copy(saved_path)
        for path in reversed(paths):
            sys.path.insert(0, path)
        sys.path.insert(0, cwd)

        # change to the desired working directory
        os.chdir(cwd)

        # load the "file" as a module
        mod = importlib.import_module(file);

        # check whether we have the desired fcn in the module
        if hasattr(mod, fcn):
            # call the desired function in the loaded module
            method = getattr(mod, fcn)
            val = method(*args)

            if fcn=="file":
                # if val is None, replace it with empty string
                if val is None:
                    val = ''
                # if val is a file-like object, read whatever is inside
                if isinstance(val,io.IOBase):
                    val.seek(0)
                    val = val.read()
                # if val is a string, treat it as utf-8
                if isinstance(val,str):
                    val = bytes(val,'utf-8')
                # if this next call does not work, it will throw an error, because
                # the thing returned by file() does not have the correct format
                val = base64.b64encode(val).decode()

            # Any function that is not 'file' or 'render' will modify 'data' and
            # should not be returning anything (because 'data' is mutable).
            if (fcn != 'file') and (fcn != 'render'):
                if val is None:
                    json_outp = json.dumps({"present": True, "val": args[-1]})
                else:
                    json_outp_passed = json.dumps({"present": True, "val": args[-1]}, sort_keys=True)
                    json_outp = json.dumps({"present": True, "val": val}, sort_keys=True)
                    if json_outp_passed != json_outp:
                        sys.stderr.write('WARNING: Passed and returned value of "data" differ in the function ' + str(fcn) + '() in the file ' + str(cwd) + '/' + str(file) + '.py.\n\n passed:\n  ' + str(args[-1]) + '\n\n returned:\n  ' + str(val) + '\n\nThere is no need to be returning "data" at all (it is mutable, i.e., passed by reference). In future, this code will throw a fatal error. For now, the returned value of "data" was used and the passed value was discarded.')
            else:
                json_outp = json.dumps({"present": True, "val": val})
        else:
            # the function wasn't present, so report this
            json_outp = json.dumps({"present": False})

        # make sure all output streams are flushed
        sys.stderr.flush()
        sys.stdout.flush()

        # write the return value (JSON on a single line)
        outf.write(json_outp)
        outf.write("\n");
        outf.flush()
