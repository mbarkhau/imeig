convertAddr = (i, link) ->
    a = $(link)
    mailAddr = a.html()
    for r in [/\[dot\]/gi, /\]dot\[/gi, /\]dot\$/gi, /\]dot\)/gi, /\]dot\(/gi]
        mailAddr = mailAddr.replace(r, '.')
    for r in [ /\[at\]/, /\]at\[/, /\]at\$/, /\%at\%/ ]
        mailAddr = mailAddr.replace(r, '@')

    a.attr('href', 'mailto:' + mailAddr).html(mailAddr)


$(document).ready(-> $("a.email").each(convertAddr))

