import Vuex from 'vuex'
import Vue from 'vue'
Vue.use(Vuex)

const ADD_TOKEN = 'ADD_TOKEN'
const REMOVE_TOKEN = 'REMOVE_TOKEN'
export default new Vuex.Store({
  state: {
      token: ''
  },
  mutations: {
    [ADD_TOKEN] (state, token) {
      sessionStorage.setItem('token', token)
      state.token = token
    },
    [REMOVE_TOKEN] (state, token) {
      sessionStorage.removeItem('token', token)
      state.token = token
    }
  }
})
