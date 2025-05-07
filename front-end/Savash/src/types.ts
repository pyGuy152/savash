import { ReactElement } from "react";


export interface Class {
    code: number;
    name: string;
    created_at: Date;
}

export function LOGOUT() {
  localStorage.removeItem("role");
  localStorage.removeItem("username");
  document.cookie = "token=; expires=Thu, 01 Jan 1970 00:00:00 UTC; path=/;";
}

export function getToken(cookie : string) {
  let property = cookie
    .split("; ")
    .find((props: string) => props.startsWith("token="));
  
    if(property){
      return property.substring(6);
    }
    else{
      return "";
    }
}

export interface Assignment {
  assignment_id : Number;
  title : string,
  description : string,
  due_date : Date,
  created_at : Date
}

export interface Tab {
  title : string,
  element : ReactElement
}