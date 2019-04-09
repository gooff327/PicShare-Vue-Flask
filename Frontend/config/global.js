import {Loading} from 'element-ui'
import axios from 'axios'

let BASE_URL = ''
let USER = {}
const UPDATE = false
const UPLOAD_FILE = ''
const HOMECONTENTS = {}
const FOLLOWINGCONTENTS = {}
const MESSAGES = {}
const COUNT = {
  admireCount: 0,
  forwardCount: 0,
  commentCount: 0,
  followCount: 0,
  sum: 0
}
let IMAGEURL = ''
const MESSAGES_CONTENT = {}
let reqList = {}
let usersList = []
let passagesList = []
let loadingInstance

isDeployEnvironment()

function isDeployEnvironment () {
  window.location.port === '8080' ? BASE_URL = 'http://127.0.0.1:5000' : BASE_URL = 'http://gooff.me'
}

async function uploadImageToPicbed (file) {
  console.log(file)
  let upInstans = axios.create()
  let picbedUrl = 'https://sm.ms/api/upload'
  var data = new FormData()
  data.append('smfile', file)
  data.append('ssl', true)
  await upInstans.post(picbedUrl, data).then(function (response) {
    IMAGEURL = response.data
  })
  return await IMAGEURL
}

function showLoading (obj) {
  if (obj) {
    loadingInstance = Loading.service(obj)
  } else {
    loadingInstance = Loading.service({text: '加载中，请耐心等待...', background: 'rgba(255,250,250,0.8)', lock: true})
  }
}

function closeLoading () {
  setTimeout(loadingInstance.close(), 0)
}

function initMessage (messages) {
  let count = {}
  count.admireCount = unreadCount(messages['admire_messages'])
  count.forwardCount = unreadCount(messages['forward_messages'])
  count.commentCount = unreadCount(messages['comment_messages'])
  count.followCount = unreadCount(messages['follow_messages'])
  count.sum = Number(count.admireCount + count.followCount + count.commentCount + count.forwardCount)
  reqList['users'] = usersList
  usersList = []
  reqList['passages'] = passagesList
  passagesList = []
  return count
}

function unreadCount (messages) {
  var count = 0
  for (var item in messages) {
    setTimeout(resolveMessage(messages[item]), 0)
    if (messages[item]['m_status'] === true) {
      count++
    }
  }
  return count
}

function resolveMessage (message) {
  usersList.push(message.uid)
  passagesList.push(message.pid)
}

export default {
  BASE_URL,
  USER,
  UPDATE,
  UPLOAD_FILE,
  HOMECONTENTS,
  FOLLOWINGCONTENTS,
  MESSAGES,
  initMessage,
  MESSAGES_CONTENT,
  COUNT,
  reqList,
  showLoading,
  closeLoading,
  uploadImageToPicbed,
  IMAGEURL
}
