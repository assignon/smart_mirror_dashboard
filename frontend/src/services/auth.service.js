import axios from "axios";

const API_URL = "http://127.0.0.1:5000/";

class AuthService {
  login(user) {
    return axios
      .post(API_URL + "login", {
        username: user.email,
        password: user.password
      })
      .then(response => {
        if (response.data.accessToken) {
          localStorage.setItem("user", JSON.stringify(response.data));
        }
        return response.data;
      });
  }
}

export default new AuthService();