import { API_LIST_DIRS, API_LIST_ALL } from "../../enviroments";


let dirname = "";


const getFiles = (endpoint: string, keyword: string): any[] => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", endpoint, false);
  xhr.send();
  let result = JSON.parse(xhr.response);
  return result[keyword];
};


export const getPhotos = (): any[] => {
  return getFiles(API_LIST_ALL + '/' + dirname, "images");
};


export const getDirs = (): any[] => {
  // TODO: figure out why it's called so often...
  let result = getFiles(API_LIST_DIRS, "dirs");
  console.log("GOT RESULT", result);
  return result;
}


export const setDir = (newDirName: string) => {
  dirname = newDirName;
};
