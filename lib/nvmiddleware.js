class Middleware {
    constructor() {
        this.variantNum = 0;
        this.totalVariantNum = -1;
    }

    nextVariant() {
        return ++this.variantNum % this.totalVariantNum;
    }

    prevVariant() {
        --this.variantNum;
        if (this.variantNum < 0) {
            this.variantNum = this.totalVariantNum - 1;
        }
        return this.variantNum;
    }

    selectVariant(num) {
        this.variantNum = num % this.totalVariantNum;
        return this.variantNum;
    }

    setTotalVariants(totalVariants) {
        this.totalVariantNum = totalVariants;
    }

    getTotalVariants() {
        return this.totalVariantNum;
    }
}

module.exports = Middleware;