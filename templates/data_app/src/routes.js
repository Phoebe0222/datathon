import Dashboard from "views/Dashboard.jsx";
import AboutUs from "views/Dashboard.jsx";

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
