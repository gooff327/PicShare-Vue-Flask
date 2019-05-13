<template>
  <div>
    <transition name="fadein">
      <el-row v-show="topBody">
        <el-col :span="24" class="middle-tab-a">
          <div class="posts">
            <span class="quantity" v-text="amounts['produces']"></span>
            <br>
            <span class="label">帖子</span>
          </div>
          <div @click="showFollowers" class="followers">
            <span class="quantity" v-text="amounts['followers']"></span>
            <br>
            <span class="followers">粉丝</span>
          </div>
          <div @click="showFollowing" class="following">
            <span class="quantity" v-text="amounts['following']"></span>
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
    <transition name="fadein">
      <div v-cloak v-show="moreView" id="moreView" class="wrapper">
        <el-row class="moreRow">
          <el-col v-for="(key,item) in contents" :key="item" :span="8"
                  class="contents">
            <img @click="contentDetail(key)" class="smallPic" v-lazy="key.img">
          </el-col>
        </el-row>
      </div>
    </transition>
    <transition name="fadein">
      <div v-cloak v-show="!moreView" id="lessView" ref="lessView" class="fullWrapper">
        <el-row>
          <el-col v-for="(key,item) in contents" :key="item" :span="24" class="contents">
            <img @click="contentDetail(key)" class="bigPic" v-lazy="key.img">
          </el-col>
        </el-row>
      </div>
    </transition>
  </div>
</template>

<script>
  import BScroll from 'better-scroll'

  export default {
    name: 'Middle',
    props: {
      uid: {
        type: Number
      },
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
        lessEl: '',
        moreEl: '',
        activeSelect: 'active-icon',
        activeMore: 'active-icon',
        activeLess: '',
        dropDown: false,
        topBody: true,
        wrapperStyle: 'wrapper'
      }
    },
    mounted () {
      this.lessEl = document.getElementById('lessView')
      this.moreEl = document.getElementById('moreView')
      this.$nextTick(() => {
        this.scrollLess = new BScroll(this.lessEl, {click: true, probeType: 3})
        this.scrollMore = new BScroll(this.moreEl, {click: true, probeType: 3})
      })
    },
    methods: {
      showMore: function () {
        this.activeLess = ''
        this.activeMore = this.activeSelect
        this.moreView = true
      },
      showLess: function () {
        this.activeMore = ''
        this.activeLess = this.activeSelect
        this.moreView = false
      },
      showFollowing: function () {
        this.$router.push({path: this.$route.path + '/followings', query: {uid: this.uid}})
      },
      showFollowers: function () {
        this.$router.push({path: this.$route.path + '/followers', query: {uid: this.uid}})
      },
      contentDetail: function (passage) {
        this.$router.push({name: 'content', params: {pid: passage.pid, passage: passage, username: passage.author}})
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

  /*.el-row{*/
  /*height: 14%;*/
  /*}*/

  .wrapper {
    position: relative;
    top: 0;
    left: 0;
    height: 60vh;
    z-index: 2;
    overflow: auto;
  }

  .fullWrapper {
    position: relative;
    bottom: 0;
    left: 0;
    top: 0;
    height: 70vh;
    z-index: 2;
    overflow: auto;
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
    top: 0.5rem;
    padding-bottom: 1rem;
    padding-top: 0.5rem;
  }

  .middle-tab-a {
    border-top: 1px solid rgba(194, 189, 167, 0.2);
    padding: 0 !important;
  }

  .middle-tab-b {
    border-top: 1px solid rgba(194, 189, 167, 0.2);
    border-bottom: 1px solid rgba(194, 189, 167, 0.2);
    padding: 0 !important;
  }

  .middle-tab-a div {
    display: block;
    padding: 0;
    margin: 0;
    width: 33%;
    text-align: center;
    line-height: 1.4rem;
    float: left;
    font-size: 0.8rem;
  }

  .middle-tab-b span {
    display: inline-block;
    padding: 0;
    margin: 0;
    width: 50%;
    text-align: center;
    line-height: 1.2rem;
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

  .el-row {
    background-color: white;
  }

</style>
