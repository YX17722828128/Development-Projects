/* eslint-disable quotes */
function sign (name, value, expiredays) {
  var exdate = new Date()
  exdate.setDate(exdate.getDate() + expiredays)
  document.cookie = name + "=" + escape(value) + ((expiredays === null) ? '' : ';expires=' + exdate.toGMTString())
}

function write (name) {
  if (document.cookie.length > 0) {
    var start = document.cookie.indexOf(name + "=")
    if (start !== -1) {
      start = start + name.length + 1
      var end = document.cookie.indexOf(";", start)
      if (end === -1) {
        end = document.cookie.length
      }
      return unescape(document.cookie.substring(start, end))
    }
  }
  return ''
}

function checkCookie (ch, value) {
  if (ch === 1) {
    sign('username', value, 365)
    return true
  } else {
    var username = write('username')
    if (username !== null && username !== '') {
      return true
    } else {
      return false
    }
  }
}

function clearCookie () {
  // eslint-disable-next-line
  var keys = document.cookie.match(/[^ =;]+(?=\=)/g)
  if (keys) {
    for (var i = keys.length; i--;) {
      document.cookie = keys[i] + '=0;expires=' + new Date(0).toUTCString()
    }
  }
}

export {
  sign,
  write,
  checkCookie,
  clearCookie
}
