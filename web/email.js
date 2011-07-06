(function() {
  var convertAddr;
  convertAddr = function(i, link) {
    var a, mailAddr, r, _i, _j, _len, _len2, _ref, _ref2;
    a = $(link);
    mailAddr = a.html();
    _ref = [/\[dot\]/gi, /\]dot\[/gi, /\]dot\$/gi, /\]dot\)/gi, /\]dot\(/gi];
    for (_i = 0, _len = _ref.length; _i < _len; _i++) {
      r = _ref[_i];
      mailAddr = mailAddr.replace(r, '.');
    }
    _ref2 = [/\[at\]/, /\]at\[/, /\]at\$/, /\%at\%/];
    for (_j = 0, _len2 = _ref2.length; _j < _len2; _j++) {
      r = _ref2[_j];
      mailAddr = mailAddr.replace(r, '@');
    }
    return a.attr('href', 'mailto:' + mailAddr).html(mailAddr);
  };
  $(document).ready(function() {
    return $("a.email").each(convertAddr);
  });
}).call(this);
