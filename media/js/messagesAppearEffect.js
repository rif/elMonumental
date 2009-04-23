var messageEffect = function (liElement) {
		MochiKit.Logging.log(liElement.id);
        MochiKit.Async.callLater(3,MochiKit.Visual.fade, liElement.id);
};

var initMessages = function () {
    MochiKit.Base.map(messageEffect,MochiKit.DOM.getElementsByTagAndClassName('li', 'message'));
};
