webpackJsonp([1],{YjjX:function(t,e){},kbM6:function(t,e){},mfOW:function(t,e,n){"use strict";var i=n("7t+N"),s=n.n(i),a={name:"carousel",data:function(){return{carouselIndex:1,interval:[],timeout:[],restart:!1,loadedIndex:0,annualRun:!1}},props:{mainItem:{type:Array}},methods:{carousel0:function(t){clearTimeout(this.timeout);var e=this;this.restart&&(this.restart=!1),this.carouselIndex=t,this.carouselIndex>this.renderItems.length?this.timeout=setTimeout(function(){e.restart=!0,e.carouselIndex=1},400):this.carouselIndex<1&&(this.timeout=setTimeout(function(){e.restart=!0,e.carouselIndex=e.renderItems.length},400))},carousel:function(t){var e=this;this.annualRun=!0,clearInterval(this.interval),this.carousel0(t),this.interval=setInterval(function(){e.carousel0(e.carouselIndex+1)},5400)},article:function(t){this.$root.article=this.renderItems[t],this.$router.push({name:"art",query:{articleId:this.renderItems[t].id}})},circleStyle:function(t){return this.carouselIndex===t||(this.carouselIndex===this.renderItems.length+t||0===this.carouselIndex&&0===t)},runCarousel:function(t){switch(t.direction){case"Right":t.stopPropagation(),this.carouselIndex>=1&&this.carousel(--this.carouselIndex);break;case"Left":t.stopPropagation(),this.carouselIndex<=this.renderItems.length&&this.carousel(++this.carouselIndex)}},sideItem:function(t){var e;switch(t){case"left":return void 0===(e=this.renderItems[this.renderItems.length-1])?{id:-1,caption:"",caption2:"加载中...",bg:""}:e;case"right":return void 0===(e=this.renderItems[0])?{id:-1,caption:"",caption2:"加载中...",bg:""}:e}}},computed:{renderItems:function(){return this.mainItem},wrapperStyle:function(){return{transition:this.wrapperTransition,transform:this.wrapperTransform}},wrapperTransition:function(){return this.restart?"":"transform .4s cubic-bezier(0.4, 0, 0, 1)"},wrapperTransform:function(){return"translate3d("+100*-this.carouselIndex/(this.renderItems.length+2)+"%, 0, 0)"},itemStyle:function(t,e){return e===this.loadedIndex&&console.log(t.target),"width: "+100/(this.renderItems.length+2)+"%; "},sideStyle1:function(){return this.itemStyle+this.sideBackground1},sideStyle2:function(){return this.itemStyle+this.sideBackground2},sideBackground1:function(){return this.loadedIndex===this.mainItem.length&&this.loadedIndex>1?this.renderItems[this.loadedIndex-1].bg:"background: #"+Math.floor(1e6*Math.random())},sideBackground2:function(){return this.loadedIndex>0?this.mainItem[0].bg:"background: #"+Math.floor(1e6*Math.random())}},watch:{mainItem:function(){var t,e,n,i,a,r;for(s()(".main-wrapper").css("width",100*(this.renderItems.length+2)+"%"),s()(".main-index").css("width",30*this.renderItems.length+"px"),s()(".main-index").css("margin","0 calc((100% - "+30*this.renderItems.length+"px) / 2)"),this.$root.adapt?t=s()("#main").height():(t=this.$root.carousel,s()("#main").css("height",t),s()(".main-item").css("height",t)),n=s()(".main-item"),a=0;a<n.length;a++){for(i=n.eq(a).children("p"),e=0,r=0;r<i.length;r++)e+=i.eq(r).height();s()(".main-item").eq(a).children("p").eq(0).css("margin-top",(t-e)/2)}},loadedIndex:function(t){t!==this.mainItem.length||this.annualRun||this.carousel(1)}},directives:{img:{inserted:function(t,e,n){var i=e.value.bg.split(/[\(\)]/)[1];if(void 0!==i){var s=Math.floor(1e6*Math.random());if(t.style.background="#"+s,e.value.index>n.context._data.loadedIndex)var a=n.context,r=setInterval(function(){if(e.value.index===a._data.loadedIndex){var n=new Image;n.src=i.substring(1,i.length-1),n.onload=function(){var n=t.style.cssText;t.style.cssText=n+e.value.bg,a._data.loadedIndex=e.value.index+1,console.log(a._data.loadedIndex)},clearInterval(r)}},100);else{var o=new Image;o.src=i.substring(1,i.length-1),o.onload=function(){var i=t.style.cssText;t.style.cssText=i+e.value.bg,n.context._data.loadedIndex=e.value.index+1,console.log(n.context._data.loadedIndex)}}}}}},beforeDestroy:function(){clearInterval(this.interval),clearTimeout(this.timeout)}},r={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"carousel"}},[n("div",{directives:[{name:"finger",rawName:"v-finger:swipe",value:t.runCarousel,expression:"runCarousel",arg:"swipe"}],attrs:{id:"main"}},[n("div",{staticClass:"main-wrapper",style:t.wrapperStyle},[n("div",{staticClass:"main-item pointer left",style:t.sideStyle1,on:{click:function(e){t.article(t.index)}}},[""!==t.sideItem("left").caption?n("p",[t._v(t._s(t.sideItem("left").caption))]):t._e(),t._v(" "),""!==t.sideItem("left").caption2?n("p",[t._v(t._s(t.sideItem("left").caption2))]):t._e()]),t._v(" "),t._l(t.renderItems,function(e,i){return n("div",{directives:[{name:"img",rawName:"v-img",value:{bg:e.bg,index:i},expression:"{'bg': item.bg, 'index': index}"}],key:i,staticClass:"main-item pointer left",style:t.itemStyle(i),on:{click:function(e){t.article(i)}}},[""!==e.caption?n("p",[t._v(t._s(e.caption))]):t._e(),t._v(" "),""!==e.caption2?n("p",[t._v(t._s(e.caption2))]):t._e()])}),t._v(" "),n("div",{staticClass:"main-item pointer left",style:t.sideStyle2,on:{click:function(e){t.article(t.index)}}},[""!==t.sideItem("right").caption?n("p",[t._v(t._s(t.sideItem("right").caption))]):t._e(),t._v(" "),""!==t.sideItem("right").caption2?n("p",[t._v(t._s(t.sideItem("right").caption2))]):t._e()])],2),t._v(" "),n("div",{staticClass:"main-index"},t._l(t.renderItems.length,function(e){return n("div",{key:e,staticClass:"main-index-item",on:{click:function(n){t.carousel(e)}}},[n("div",{staticClass:"index-circle pointer",class:{active:t.circleStyle(e)}})])}))])])},staticRenderFns:[]};var o=n("VU/8")(a,r,!1,function(t){n("kbM6")},"data-v-4ebe8557",null);e.a=o.exports},s8dJ:function(t,e,n){"use strict";Object.defineProperty(e,"__esModule",{value:!0});var i=n("7t+N"),s=n.n(i),a=n("mfOW"),r=n("nq5D"),o={name:"center",data:function(){return{mainItem:[],mainContent:[{caption:"全面、领先的解决方案",caption2:"产品覆盖数通安全、传输接入、IT、企业云通信、网络能源、云软件，能针对不同需求提供完整的解决方案。",learn:!0},{caption:"丰富的项目经验",caption2:"多年来，凭借卓越的产品和优秀的服务，公司已完成A、B、C等多个大型项目建设。"},{caption:"专业、可靠的技术支持",caption2:"专业的技术团队为政府、企业的数字化、智慧化转型保驾护航。"},{caption:"卓越的公司团队",caption2:"",learn:!0}],solutions:["数通安全","传输输入","IT","企业云通信","网络能源","云软件"],solutionList:[],solutionIndex:1,solutionStatus:!1}},methods:{renderPage:function(t){return t%2==0?"background-color: white;":"background-color: #F0F2F5;"},hideList:function(){this.$root.eventHub.$emit("hide")},learn:function(t){switch(t){case 0:this.$router.push({path:"/products"});break;case 3:this.$router.push({path:"/introduction"})}},showSolution:function(){for(var t=this,e=function(e){setTimeout(function(){t.solutionList.push(t.solutions[e]),t.$nextTick()},100*e)},n=0;n<this.solutions.length;n++)e(n)}},components:{Carousel:a.a,foot:r.a},created:function(){var t=this;s.a.ajax({async:!0,url:"/carousel/",type:"GET",data:{},success:function(e){for(var n=[],i=0;i<e.length;i++)-1===e[i].title.indexOf("≮")?n.push({id:e[i].news_id,caption:"",caption2:e[i].title.split("≮")[0],bg:e[i].bg}):n.push({id:e[i].news_id,caption:e[i].title.split("≮")[0],caption2:e[i].title.split("≮")[1],bg:e[i].bg});t.mainItem=n}})},mounted:function(){var t=this;this.$root.adapt||this.$root.height>600&&(this.showSolution(),this.solutionStatus=!0),this.$root.eventHub.$on("showSolution",function(){t.solutionStatus||(t.showSolution(),t.solutionStatus=!0)})}},c={render:function(){var t=this,e=t.$createElement,n=t._self._c||e;return n("div",{attrs:{id:"center"},on:{touchstart:t.hideList}},[n("Carousel",{attrs:{"main-item":t.mainItem}}),t._v(" "),n("div",{staticClass:"main-content"},[t._l(t.mainContent,function(e,i){return n("div",{key:i,staticClass:"page",style:t.renderPage(i)},[""!==e.caption?n("p",{staticClass:"title"},[t._v(t._s(e.caption))]):t._e(),t._v(" "),""!==e.caption2?n("p",{staticClass:"interpret"},[t._v(t._s(e.caption2))]):t._e(),n("br"),t._v(" "),e.learn?n("p",{staticClass:"learnMore pointer",on:{click:function(e){t.learn(i)}}},[t._v("了解更多")]):t._e(),t._v(" "),0===i?n("div",{staticClass:"solution-circle-bar",attrs:{id:"solution-bar"}},[n("div",{staticClass:"solution-circle-wrapper"},[n("transition-group",{attrs:{name:"solution"}},t._l(t.solutionList,function(e,i){return n("div",{key:i,staticClass:"solution-circle pointer left"},[n("p",[t._v(t._s(e))])])}))],1)]):t._e()])}),t._v(" "),n("foot")],2)],1)},staticRenderFns:[]};var l=n("VU/8")(o,c,!1,function(t){n("YjjX")},"data-v-be223e22",null);e.default=l.exports}});
//# sourceMappingURL=1.cf1c03448fe2a8e76ac1.js.map