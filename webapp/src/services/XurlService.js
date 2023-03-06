import Axios from 'axios';

const XurlService = {
    get(url){
        return Axios.get(url);     
    },
    getSubjectItems(baseURI, subjectType){
        const url = `${baseURI}/subject/${subjectType}`;
        return Axios.get(url);     
    }
}

export default XurlService;