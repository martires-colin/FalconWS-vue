import { createStore } from 'vuex'

export default createStore({
  state: {
    user: {
      full_name: null,
      email: null,
      idp_name: null,
      access_token: null,
      id_token_jwt: null
    },
    site_1: null,
    site_2: null
  },
  getters: {
  },
  mutations: {
    SET_USER(state, data) {
      state.user.full_name = data.full_name
      state.user.email = data.email
      state.user.idp_name = data.idp_name
      state.user.access_token = data.access_token
      state.user.id_token_jwt = data.id_token_jwt
      state.site_1 = data.site_1
      state.site_2 = data.site_2
    },
  },
  actions: {
    async setUser({ commit }, user_info) {
      console.log("SETTING USER")
      commit('SET_USER', {
        full_name: user_info.full_name,
        email: user_info.email,
        idp_name: user_info.idp_name,
        access_token: user_info.access_token,
        id_token_jwt: user_info.id_token_jwt,
        site_1: user_info.site1_info,
        site_2: user_info.site2_info
      })
    },
  },
  modules: {
  }
})
