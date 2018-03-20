export const SetAuth = (state, _auth) => {
  state.user_ = _auth.user
  state.token_ = _auth.token
}
