
define(["underscore", "backbone", "mustache", "AdaptiveTestHelper", "text!AdaptiveTestView.html"], function(_, Backbone, Mustache, AdaptiveTestHelper, AdaptiveTestViewTemplate) {

    var AdaptiveTestView = Backbone.View.extend({
        tagName: 'div',

        initialize: function() {
            this.tInstances = this.options.tInstances;
            this.listenTo(this.model, "change", this.render);
            this.listenTo(this.tInstances, "change", this.render);
        },

        render: function() {
            var that = this;
            var data = {};
            data.title = this.model.get("title");
            data.tid = this.model.get("tid");

            var tInstance = this.tInstances.findWhere({tid: this.model.get("tid")});
            if (tInstance === undefined)
                return;
            data.tiid = tInstance.get("tiid");
            var score = tInstance.get("score");
            data.score = AdaptiveTestHelper.renderHWScore(tInstance);
            data.scoreBar = AdaptiveTestHelper.renderScoreBar(score);
            var dueDate = new Date(that.model.get("dueDate"));
            data.dueDate = AdaptiveTestHelper.renderDueDate(dueDate);

            var html = Mustache.render(AdaptiveTestViewTemplate, data);
            this.$el.html(html);
        },

        close: function() {
            this.remove();
        },
    });

    return AdaptiveTestView;
});
