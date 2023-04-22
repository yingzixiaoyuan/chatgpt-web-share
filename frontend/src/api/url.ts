enum ApiUrl {
  Register = "/auth/register",
  Login = "/auth/login",
  Logout = "/auth/logout",
  UserInfo = "/user/me",
  RegisterUser = "/register",
  
  Conversation = "/conv",
  UserList = "/user",

  ServerStatus = "/status",
  SystemInfo = "/system/info",
  SystemRequestStatistics = "/system/request_statistics",
  ProxyLogs = "/system/proxy_logs",
  ServerLogs = "/system/server_logs"
}

export default ApiUrl;
