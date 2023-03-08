import Axios from 'axios';

const XurlService = {
    get(url){
        return Axios.get(url);     
    },
    getInfo(baseURI){
        const url = `${baseURI}/info`;
        return Axios.get(url);     
    },
    getSubjectItems(baseURI, subjectType){
        const url = `${baseURI}/subject/${subjectType}`;
        return Axios.get(url);     
    },
    getSubjectItem(baseURI, subjectType, subjectId){
        const url = `${baseURI}/subject/${subjectType}/${subjectId}`;
        return Axios.get(url);     
    }
}

export default XurlService;