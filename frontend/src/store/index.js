import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      full_name: null,
      email: null,
      idp_name: null
    },
    // Future Local Session Variables
    // site_1: {
    //   full_name: null,
    //   email: null,
    //   idp_name: null
    // },
    // site_2: {
    //   full_name: null,
    //   email: null,
    //   idp_name: null
    // }
  },
  getters: {
  },
  mutations: {
    SET_USER(state, data) {
      state.user.full_name = data.full_name
      state.user.email = data.email
      state.user.idp_name = data.idp_name
    },
  },
  actions: {
  },
  modules: {
  }
})
