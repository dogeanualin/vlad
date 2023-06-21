(function (global, factory) {
  typeof exports === 'object' && typeof module !== 'undefined' ? module.exports = factory() :
  typeof define === 'function' && define.amd ? define(factory) :
  (global = typeof globalThis !== 'undefined' ? globalThis : global || self, global.config = factory());
})(this, (function () { 'use strict';

  const configQueryMap={"navbar-vertical-collapsed":"cmsAtiIsNavbarVerticalCollapsed","color-scheme":"cmsAtiTheme","navigation-type":"cmsAtiNavbarPosition","vertical-navbar-appearance":"cmsAtiNavbarVerticalStyle","horizontal-navbar-shape":"cmsAtiNavbarTopShape","horizontal-navbar-appearance":"cmsAtiNavbarTopStyle"},initialConfig={cmsAtiIsNavbarVerticalCollapsed:!1,cmsAtiTheme:"light",cmsAtiNavbarTopStyle:"default",cmsAtiNavbarVerticalStyle:"default",cmsAtiNavbarPosition:"vertical",cmsAtiNavbarTopShape:"default",cmsAtiIsRTL:!1},CONFIG={...initialConfig},setConfig=(e,a=!0)=>{Object.keys(e).forEach((o=>{CONFIG[o]=e[o],a&&localStorage.setItem(o,e[o]);}));},resetConfig=()=>{Object.keys(initialConfig).forEach((e=>{CONFIG[e]=initialConfig[e],localStorage.setItem(e,initialConfig[e]);}));},urlSearchParams=new URLSearchParams(window.location.search),params=Object.fromEntries(urlSearchParams.entries());console.log({params:params}),Object.keys(params).length>0&&Object.keys(params).includes("theme-control")&&(resetConfig(),Object.keys(params).forEach((e=>{configQueryMap[e]&&localStorage.setItem(configQueryMap[e],params[e]);}))),Object.keys(CONFIG).forEach((e=>{if(null===localStorage.getItem(e))localStorage.setItem(e,CONFIG[e]);else try{setConfig({[e]:JSON.parse(localStorage.getItem(e))});}catch{setConfig({[e]:localStorage.getItem(e)});}})),JSON.parse(localStorage.getItem("cmsAtiIsNavbarVerticalCollapsed"))&&document.documentElement.classList.add("navbar-vertical-collapsed"),"dark"===localStorage.getItem("cmsAtiTheme")&&document.documentElement.classList.add("dark"),"horizontal"===localStorage.getItem("cmsAtiNavbarPosition")&&document.documentElement.classList.add("navbar-horizontal"),"combo"===localStorage.getItem("cmsAtiNavbarPosition")&&document.documentElement.classList.add("navbar-combo");var config = {config:CONFIG,reset:resetConfig,set:setConfig};

  return config;

}));
//# sourceMappingURL=config.js.map
