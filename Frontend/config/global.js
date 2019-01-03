const BASE_URL = 'http://204.44.85.176:8000'
var USER = {}
var UPDATE = false
var UPLOAD_FILE = ''
var HOMECONTENTS = {}
var FOLLOWINGCONTENTS = {}
var MESSAGES = {}
var COUNT = {
  admireCount: 0,
  privateCount: 0,
  forwardCount: 0,
  commentCount: 0,
  followCount: 0,
  sum: 0
}

function initMessage (messages) {
  let count = {}
  console.log('messages', messages)
  count.admireCount = unreadCount(messages['admire_messages'])
  count.privateCount = unreadCount(messages['private_messages'])
  count.forwardCount = unreadCount(messages['forward_messages'])
  count.commentCount = unreadCount(messages['comment_messages'])
  count.followCount = unreadCount(messages['follow_messages'])
  count.sum = Number(count.admireCount + count.privateCount + count.followCount + count.commentCount + count.forwardCount)
  console.log('sum',count.sum)
  return count
}

function unreadCount (Messages) {
  var count = 0
  for (var item in Messages) {
    console.log(Messages[item]['m_status'] === true)
    if (Messages[item]['m_status'] === true) {
      count++
    }
  }
  console.log(count)
  return count
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
  COUNT
}
