import Dashboard from "./views/Dashboard";
import AboutUs from "./views/Dashboard";

var routes = [
  {
    path: "/dashboard",
    name: "Dashboard",
    component: Dashboard,
    layout: "/user"
  },
  {
    path: "/aboutus",
    name: "About us",
    component: AboutUs,
    layout: "/user"
  }
];

export default routes;
