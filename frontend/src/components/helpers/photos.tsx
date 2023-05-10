import { useParams } from 'react-router';

import { API_LIST_DIRS, API_LIST_ALL } from "../../enviroments";


let dirname = "";


const getFiles = (endpoint: string): any[] => {
  const xhr = new XMLHttpRequest();
  xhr.open("GET", endpoint, false);
  xhr.send();
  const json = JSON.parse(xhr.response);
  return json["files"];
};


export const getPhotos = (): any[] => {
  // get the photos -- one case or the other
  if (dirname === "") {
    // show the available dirs
    let result = getFiles(API_LIST_DIRS);
    return result;
  } else {
    // show the files in the dir
    let result = getFiles(API_LIST_ALL + '/' + dirname);
    return result;
  }
};


export const setDir = (newDirName: string): string => {
  // go into the specific directory
  if (dirname === "") {
    dirname = newDirName;
    return "";
  } else {
    return dirname;
  }
};
