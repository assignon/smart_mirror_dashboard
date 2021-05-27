import Vue from "vue";
import VueRouter from "vue-router";
import Login from "../views/Login.vue";
import Checkin from "../views/checkin";
import Gastenlijst from "@/views/Ingecheckt";
import Clients from "@/views/Clients";
import Instellingen from "@/views/Instellingen";
import Admin from "@/views/Admin";

Vue.use(VueRouter);

const routes = [
  {
    path: "/",
    redirect: "Login"
  },
  {
    path: "/login",
    name: "Login",
    component: Login
  },
  {
    path: "/checkin",
    name: "Checkin",
    component: Checkin
  },
  {
    path: "/ingecheckt",
    name: "Ingecheckt",
    component: Gastenlijst
  },
  {
    path: "/clients",
    name: "Clients",
    component: Clients
  },
  {
    path: "/instellingen",
    name: "Instellingen",
    component: Instellingen
  },
  {
    path: "/Admin",
    name: "Admin",
    component: Admin
  }
  // {
  //   path: "/about",
  //   name: "About",
  //   // route level code-splitting
  //   // this generates a separate chunk (about.[hash].js) for this route
  //   // which is lazy-loaded when the route is visited.
  //   component: () =>
  //     import(/* webpackChunkName: "about" */ "../views/About.vue")
  // }
];

const router = new VueRouter({
  mode: "history",
  base: process.env.BASE_URL,
  routes
});

export default router;
