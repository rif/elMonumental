var messageEffect = function (liElement) {
		MochiKit.Logging.log(liElement.id);
        MochiKit.Visual.appear(liElement.id);
};

var initMessages = function () {
    MochiKit.Base.map(messageEffect,MochiKit.DOM.getElementsByTagAndClassName('li', 'message'));
};
