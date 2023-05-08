import { API_LIST_DIRS, API_LIST_ALL } from "../../enviroments";


export const getDirs = (): any[] => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", API_LIST_DIRS, false);
  xhr.send();
  const json = JSON.parse(xhr.response);
  return json["files"];
};


export const getDirPhotos = (dir: string): any[] => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", API_LIST_ALL + '/' + dir, false);
  xhr.send();
  const json = JSON.parse(xhr.response);
  console.log("GOT JSON", json);
  return json["files"];
};
