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
      <div v-cloak v-show="moreView"  class="wrapper">
        <el-row class="moreRow">
          <el-col v-for="(key,item) in contents" :key="item" :span="8" class="contents">
            <img class="smallPic" :src="key.img">
          </el-col>
        </el-row>
      </div>
    </transition>
    <transition name="fadein">
      <div v-cloak v-show="!moreView">
        <el-row>
          <el-col v-for="(key,item) in contents" :key="item" :span="24" class="contents">
            <img class="bigPic" :src="key.img">
          </el-col>
        </el-row>
      </div>
    </transition>
  </div>
</template>

<script>

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
        activeSelect: 'active-icon',
        activeMore: 'active-icon',
        activeLess: '',
        dropDown: false,
        topBody: true,
        wrapper1: 'wrapper',
        wrapper2: '',
        wrapperStyle: 'wrapper'
      }
    },
    methods: {
      showMore: function () {
        this.activeLess = ''
        this.activeMore = this.activeSelect
        this.moreView = true
        this.wrapper1 = 'wrapper'
        this.wrapper2 = ''
      },
      showLess: function () {
        this.activeMore = ''
        this.activeLess = this.activeSelect
        this.moreView = false
        this.wrapper1 = ''
        this.wrapper2 = 'wrapper'
      },
      showFollowing: function () {
        this.$router.push({path: this.$route.path + '/followings', query: {uid: this.uid}})
      },
      showFollowers: function () {
        this.$router.push({path: this.$route.path + '/followers', query: {uid: this.uid}})
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
    position: relative;
    top: 0;
    left: 0;
    height: 50vh;
    z-index: 2;
    overflow: auto;
  }

  .fullWrapper {
    position: relative;
    top: 0;
    left: 0;
    height: 90vh;
    z-index: 2;
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

</style>
