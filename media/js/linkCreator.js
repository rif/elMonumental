var convertSPAN = function (spanElem) {
        var doReplace = function (req) {
            $(spanElem.id).innerHTML = req.responseText;
        };

        var doReplaceError = function () {
            $(spanElem.id).innerHTML = 'Error!!!';
        };

        var res = MochiKit.Async.doSimpleXMLHttpRequest('links/' + spanElem.id);
        res.addCallbacks(doReplace,doReplaceError);
};

var initpage = function () {
    MochiKit.Base.map(convertSPAN,MochiKit.DOM.getElementsByTagAndClassName('span', 'async'));
};
