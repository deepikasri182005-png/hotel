function login(email, password) {

  if (!email || !password) {

    return { error: "Email and password required" };

  }

  // verify credentials

  return { success: true, token: "abc123" };

}



function logout(token) {

  // invalidate token

  return { success: true };

}



function resetPassword(email) {

  // send reset email

  return { success: true };

}
