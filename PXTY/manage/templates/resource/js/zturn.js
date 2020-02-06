(function (win) {
  var zturn = function (turn) {
    this.turn = turn
    this.zturn = document.getElementById(turn.id)
    this.X = 0
    this.zturnitem = document.getElementsByClassName('zturn-item')
    this.num_li = this.zturnitem.length// 轮播元素个数 zturnPy为每个的偏移量
    this.zturnPy = turn.Awidth / (this.num_li - 1)
    this.init()
    this.turn_()
    return this
  }
  zturn.prototype = {
    constructor: zturn,
    init: function () {
      var self = this
      for (var index = 0; index < this.zturnitem.length; index++) {
        var element = this.zturnitem[index]
        var rt = 1 // 1:右侧：-1：左侧
        // eslint-disable-next-line no-mixed-operators
        if ((index - self.X) > self.num_li / 2 || (index - self.X) < 0 && (index - self.X) > (-self.num_li / 2)) { rt = -1 }// 判断元素左侧还是右侧
        var i = Math.abs(index - self.X) // 取绝对值
        if (i > self.num_li / 2) { i = parseInt(self.X) + parseInt(self.num_li) - index }// i:是左或者右的第几个
        if ((index - self.X) < (-self.num_li / 2)) { i = self.num_li + index - self.X }
        var cssText = 'z-index: ' + (self.num_li - i) + '; '
        cssText += 'opacity: ' + Math.pow(self.turn.opacity, i) + '; '
        cssText += 'margin-left: ' + (-self.turn.width / 2 + self.zturnPy * rt * i) + 'px; '
        cssText += 'transform: scale(' + Math.pow(self.turn.scale, i) + '); '
        element.style.cssText = cssText
        element.setAttribute('index', index + '')
      }
    },
    turn_: function () {
      var self = this
      for (var i = 0; i < self.zturnitem.length; i++) {
        self.zturnitem[i].addEventListener('click', function () {
          self.X = this.attributes['index'].value
          self.init()
        })
      }
    }
  }
  win.zturn = zturn
}(window, document))
