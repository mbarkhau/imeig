function convertMailAddresses() {
    var mailLinks = $("a.email");
    $.each(mailLinks, convertMailAddress);
}

function convertMailAddress(i, link) {
    var a = $(link);
    var mailAddr = a.html();
    mailAddr = mailAddr.replace(/\[dot\]/gi, '.');
    mailAddr = mailAddr.replace(/\]dot\[/gi, '.');
    mailAddr = mailAddr.replace(/\]dot\$/gi, '.');
    mailAddr = mailAddr.replace(/\]dot\)/gi, '.');
    mailAddr = mailAddr.replace(/\]dot\(/gi, '.');
    mailAddr = mailAddr.replace(/\[at\]/, '@');
    mailAddr = mailAddr.replace(/\]at\[/, '@');
    mailAddr = mailAddr.replace(/\]at\$/, '@');
    mailAddr = mailAddr.replace(/\%at\%/, '@');
    a.attr('href', 'mailto:' + mailAddr);
    a.html(mailAddr);
}

$(document).ready(convertMailAddresses);
