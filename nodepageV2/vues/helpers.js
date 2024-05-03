const maxNtpOffsetHost = function(ntpStatus) {
    let maxOffsetHost = null
    for (let host in ntpStatus) {
        if (maxOffsetHost === null || ntpStatus[host][6] > ntpStatus[maxOffsetHost][6])
            maxOffsetHost = host
    }
    return maxOffsetHost
}

const prettyMaxNtpOffset = function(ntpStatus) {
    let maxOffsetHost = maxNtpOffsetHost(ntpStatus)
    return maxOffsetHost + ": " + (Math.trunc(ntpStatus[maxOffsetHost][6] * 1000.0 * 1000.0) / 1000.0) + "ms"
}

const prettyPublishRate = function(published_at_ns) {
    if (published_at_ns.length < 2) return "?Hz"
    let periods_ns = []
    for (let i = 0; i < published_at_ns.length - 1; ++i) {
        if (i > 0 && (published_at_ns[0] - published_at_ns[i]) > 10 * 1000 * 1000 * 1000) break
        periods_ns.push(published_at_ns[i] - published_at_ns[i + 1])
    }

    avg_period_s = (periods_ns.reduce((a, b) => a + b) / periods_ns.length) / (1000.0 * 1000.0 * 1000.0)
    return "" + Math.trunc((1.0 / avg_period_s) * 1000.0) / 1000.0 + "Hz"
}

const prettyPublishPersist = function(numPublished, numPersisted) {
  return "" + numPublished + "/" + numPersisted
}

function HtmlObject(html) {
  this.html = html
}

function ImgObject(src) {
  this.src = src
}

const videoFeedImg = function(webappUrl) {
  return new ImgObject(webappUrl + "/video_jpeg")
}

const uriNodeName = function(nodeName) {
  if (nodeName.startsWith('/')) {
    return nodeName.substring(1)
  }
  return nodeName
}

const isNullOrEmptyStr = function(val) {
  return val == null || val.trim() == ""
}

const toStringy = function(val) {
  return val == null ? "" : val.trim()
}

const throwAlertResponseErr = function(response) {
  err = new Error("" + response.status + ": " + response.statusText)
  alert(err.message)
  throw err
}