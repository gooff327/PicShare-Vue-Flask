<template>
  <div>
    <transition name="fadein">
      <el-row>
        <el-col :span="24" class="middle-tab-a">
          <div class="posts">
            <span class="quantity" v-text="amounts['produces']"></span>
            <br>
            <span class="label">帖子</span>
          </div>
          <div class="followers">
            <span class="quantity">9</span>
            <br>
            <span class="followers">粉丝</span>
          </div>
          <div class="following">
            <span class="quantity">10</span>
            <br>
            <span class="following">关注</span>
          </div>
        </el-col>
        <el-col :span="24" class="middle-tab-b">
          <span @click="showMore" :class="activeMore" class="fa fa-th"></span><span @click="showLess"
                                                                                    :class="activeLess"
                                                                                    class="fa fa-navicon"></span>
        </el-col>
        <transition name="fadein">
          <span class="dropDown" v-show="dropDown"> <i class="el-icon-loading"></i>刷新数据</span>
        </transition>
      </el-row>
    </transition>
    <div v-cloak v-show="moreView" ref="wrapper" :class="wrapperStyle">
      <el-row class="moreRow">
        <el-col v-for="(key,item) in contents" :key="item" :span="8" class="contents">
          <img class="smallPic" :src="['data:Image/png;base64,'+key.img]">
        </el-col>
      </el-row>
    </div>
    <div v-cloak v-show="!moreView" ref="wrappers" :class="wrapperStyle">
      <el-row>
        <el-col v-for="(key,item) in contents" :key="item" :span="24" class="contents">
          <img class="bigPic" :src="['data:Image/png;base64,'+key.img]">
        </el-col>
      </el-row>
    </div>
  </div>
</template>

<script>
  import BScroll from 'better-scroll'

  export default {
    name: 'Middle',
    props: {
      amounts: {
        type: Object
      },
      contents: {
        type: Object
      }
    },
    data () {
      return {
        moreView: true,
        activeSelect: 'active-icon',
        activeMore: 'active-icon',
        activeLess: '',
        wrapperStyle: 'wrapper',
        dropDown: false,
        topBody: true
      }
    },
    mounted () {
      this.$nextTick(() => {
        if (!this.scroll) {
          this.scroll = new BScroll(this.$refs.wrapper, {
            click: true,
            bounce: true,
            scrollY: true,
            topBody: true,
            probeType: 3,
            pullUpLoad: {
              threshold: 0
            },
            pullDownRefresh: {
              threshold: 20
            }
          })
          this.scroll.on('scroll', (position) => {
            if (!this.scroll.isInTransition && !this.scroll.isAnimating && position.y > 20) {
              this.dropDown = true
            } else if (position.y < 0) {
              this.$emit('closeTop', false)
              this.wrapperStyle = 'fullWrapper'
            } else if (position.y > 0) {
              this.wrapperStyle = 'wrapper'
              this.$emit('closeTop', true)
            } else {
              this.dropDown = false
            }
          })
          this.scroll.on('pullingDown', () => {
            this.topBody = true
            this.$emit('refresh')
            this.$emit('closeTop', true)
            setTimeout(() => {
              this.scroll.finishPullDown()
              this.scroll.refresh()
            }, 200)
          })
          this.scroll.on('pullingUp', () => {
            console.log('加载数据！')
            this.$emit('loadData')
            setTimeout(() => {
              this.scroll.finishPullUp()
              this.scroll.refresh()
            }, 200)
          })
        } else {
          this.scroll.refresh()
        }
      })
    },
    methods: {
      showMore: function () {
        console.log(1)
        this.activeLess = ''
        this.activeMore = this.activeSelect
        this.moreView = true
      },
      showLess: function () {
        this.activeMore = ''
        this.activeLess = this.activeSelect
        this.moreView = false
      }
    }
  }
</script>

<style scoped>
  .slide-enter-active, .slide-leave-active {
    transition: transform 0.4s ease;
  }

  .slide-enter, .slide-leave {
    transform: translate3d(100%, 0, 0);
  }

  .fadein-enter-active, .fadein-leave-active {
    transition: opacity .5s
  }

  .fadein-enter, .fadein-leave-to {
    opacity: 0
  }

  .wrapper {
    position: fixed;
    top: 0;
    left: 0;
    height: 53vh;
    overflow: hidden;
  }
  .moreRow {
    background: white;
  }
  .dropDown {
    color: #34BE5B;
    display: inline-block;
    width: 100%;
    text-align: center;
    position: relative;
    top: 10px;
    padding-bottom: 20px;
  }

  .fullWrapper {
    position: relative;
    top: 0;
    height: 60vh;
  }

  .middle-tab-a {
    border-top: 1px solid gainsboro;
    padding: 0 !important;
  }

  .middle-tab-b {
    border-top: 1px solid gainsboro;
    border-bottom: 1px solid gainsboro;
    padding: 0 !important;
  }

  .middle-tab-a div {
    display: block;
    padding: 0;
    margin: 0;
    width: 33%;
    text-align: center;
    line-height: 2rem;
    float: left;
  }

  .middle-tab-b span {
    display: inline-block;
    padding: 0;
    margin: 0;
    width: 50%;
    text-align: center;
    line-height: 2rem;
    margin-top: 0.4rem;
    margin-bottom: 0.4rem;
  }

  .wrapper {
    margin-top: 10px;
    position: relative;
  }

  [v-cloak] {
    display: none;
  }

  .smallPic {
    width: 97%;
    height: 17.65vh;
    object-fit: cover;
    border-left: white 1px solid;
    border-right: white 1px solid;
  }

  .bigPic {
    width: 100%;
    height: auto;
    object-fit: cover;
    border-radius: 4px;
  }

  .active-icon {
    color: #409EFF;
  }

</style>
