<!--suppress ALL -->
<template>
  <transition appear>
    <div>
      <div ref="wrapper" class="wrapper">
        <div class="contentWrapper">
          <el-card shadow="hover" :body-style="{padding: '6px' }" class="item" v-for="(key,item) in contents"
                   :key="item">
            <div class="headbar">
              <img @click="showUserDetails(key.author)" class="avatar" v-lazy="key.uavatar"
                   alt="">
              <span class="username">{{key.author}}</span>
            </div>
            <section class="contentImage" ondblclick="likeEvent(key)">
              <img onmouseover="displayDesc" class="innerPic" v-lazy="key.img" :preview="key.pid"
                   alt="">
            </section>
            <section @click="contentDetail(key)" class="descWrapper">
              <span class="imageDesc" v-if="key.desc.length<40">{{key.desc}}</span>
              <span class="imageDesc" v-else>{{key.desc.slice(0,37)}} ... ...</span>
            </section>
            <section class="bottom">
              <span  @click="contentDetail(key)" class="bottomText">{{key.date.slice(11,-3)}}</span>
              <span class="botttomIcon">
                <img v-if="admire[key.pid] ===true" @click="likeEvent(key)"
                     src="../../../static/icons/admire_colored.svg" style="width: 1.5rem" alt="">
                <img v-else @click="likeEvent(key)" src="../../../static/icons/admire.svg" style="width: 1.5rem" alt="">
                <img @click="commentEvent(key.pid,key.uid)" src="../../../static/icons/comment.svg"
                     style="width: 1.5rem" alt="">
                <img @click="forwardEvent(key)" src="../../../static/icons/forward.svg"
                     style="width: 1.5rem;color: green;" alt="">
           </span>
            </section>
          </el-card>
        </div>
      </div>
    </div>
  </transition>
</template>

<script>
  import comment from '../../components/Common/comment'
  import BScroll from 'better-scroll'
  import store from '../../vuex/user'

  export default {
    data () {
      return {
        showContents: true,
        dropDown: false,
        updatePanel: false,
        emptyContent: true,
        refreshData: {},
        scrollpos: 0,
        admire: {}
      }
    },
    components: {
      'comment': comment
    },
    created: function () {
      this.getAdmireList()
    },
    watch: {
      $route (to, from) {
        this.getAdmireList()
        if (from.path === '/following') {
          let position = this.scroll.y
          store.commit('changefPosition', position)
        }
        if (to.path === '/following') {
          this.scroll.refresh()
          this.scroll.scrollTo(0, store.state.positions.fPosition)
        }
      }
    },
    mounted () {
      this.$nextTick(() => {
        this.initHomeScroll()
      })
    },
    methods: {
      initHomeScroll: function () {
        if (!this.scroll) {
          this.scroll = new BScroll(this.$refs.wrapper, {
            click: true,
            bounce: true,
            scrollY: true,
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
            } else {
              this.dropDown = false
            }
          })

          this.scroll.on('pullingDown', () => {
            this.$emit('refresh')
            setTimeout(() => {
              this.scroll.finishPullDown()
              this.scroll.refresh()
            }, 200)
          })
          this.scroll.on('pullingUp', () => {
            this.$emit('loadMore')
            setTimeout(() => {
              this.scroll.finishPullUp()
              this.scroll.refresh()
            }, 200)
          })
        } else {
          this.scroll.refresh()
        }
        // this.setHeight()
      },
      getAdmireList: function () {
        var url = this.GLOBAL.BASE_URL + '/api/v1/admire'
        this.$axios.get(url).then(function (res) {
          if (res.data.code === 521) {
            this.admire = res.data.admire
          }
        }.bind(this))
      },
      showUserDetails: function (username) {
        this.GLOBAL.showLoading()
        this.$router.push(`/user/${username}`)
      },
      likeEvent: function (key) {
        this.admire[key.pid] === true ? this.admire[key.pid] = false : this.admire[key.pid] = true
        let url = this.GLOBAL.BASE_URL + '/api/v1/admire'
        let admireList = JSON.stringify(this.admire)
        let admireThis = JSON.stringify({pid: key.pid, uid: key.uid, result: this.admire[key.pid]})
        let data = {
          admireList: admireList,
          admireThis: admireThis
        }
        this.$axios.post(url, data, {headers: {'Content-Type': 'Application/json'}}).then(function (response) {
          if (response.data.code === 520 && this.admire[key.pid] === true) {
          }
        }.bind(this))
      },
      commentEvent: function (pid, vid) {
        this.$router.push({name: 'comment', params: {pid: pid, vid: vid}})
      },
      forwardEvent: function (key) {
        this.$router.push({name: 'forward', params: {pid: key.pid, passage: key}})
      },
      contentDetail: function (passage) {
        this.$router.push({name: 'content', params: {pid: passage.pid, passage: passage, username: passage.author}})
      }
    },
    props: {
      contents: {
        type: Object
      }
    },
    name: 'contents'
  }
</script>
<style scoped>
  [v-cloak] {
    display: none;
  }

  .fadein-enter-active, .fadein-leave-active {
    transition: opacity .5s
  }

  .fadein-enter, .fadein-leave-to {
    opacity: 0
  }

  .headbar {
    display: inline-block;
    vertical-align: top;
    font-size: 20%;
    margin-bottom: -0.1rem;
    margin-top: -0.2rem;
    width: 100%;
    margin-left: 0.6rem;
    position: relative;
    z-index: 2;
  }

  .headers {
    position: fixed;
    top: 0rem;
    z-index: 1;
  }

  .wrapper {
    position: absolute;
    z-index: 2;
    left: 0;
    top: 0px;
    overflow: hidden;
    max-height: 94vh;
    border: 1px solid white;
  }

  .descWrapper {
    margin-top: 0.6rem;
    margin-left: 0.6rem;
  }

  .imageDesc {
    display: block;
    font-size: 0.8rem;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
  }

  .username {
    display: inline-block;
    max-width: 70%;
    font-family: "Helvetica Neue", Helvetica, "PingFang SC", "Hiragino Sans GB", "Microsoft YaHei", "微软雅黑", Arial, sans-serif;
    font-size: 0.7rem;
    padding-left: 0.2rem;
  }

  .avatar {
    display: inline-block;
    width: 1.8rem;
    height: 1.8rem;
    border-radius: 50%;
    transform: translate(0, 45%);
    border: 2px solid white;
  }

  .bottomText {
    font-size: 0.6rem;
    color: gray;
    margin: 0;
    padding: 0;
    margin-left: 0.6rem;
  }

  .botttomIcon {
    display: inline-block;
    float: right;
    padding-right: 0.6rem;
    margin-bottom: 0.6rem;
  }

  .fa {
    padding-right: 0.3rem;
    padding-left: 0.3rem;
    /*padding-bottom: 0.2rem;*/
  }

  .contentImage {
    margin-top: 0.2rem;
    width: 96vw;
    height: 54vw;
    position: relative;
  }

  .contentImage img {
    width: 100%;
    height: 100%;
    object-fit: cover;
  }

  .emptyContent {
    display: block;
    text-align: center;
    width: 100;
  }

  .innerPic {
    width: auto;
    height: auto;
    max-width: 100%;
    max-height: 100%;
    border-radius: 4px;
  }

  .fa-heart:touch {
    animation: admire 1s normal;
  }

  @keyframes admire {
    0% {
      transform: scale(1, 1)
    }
    20% {
      transform: scale(2.4, 2.4)
    }
    100% {
      transform: scale(1, 1)
    }
  }

  .fa-heart-o:hover {
    transition: color 1.5s;
  }

  .moreInfo {
    display: inline-block;
    width: 100%;
    text-align: center;
    color: #34BE5B;
  }

  .contentWrapper {
    background-color: #cfcfc0;
  }
</style>
