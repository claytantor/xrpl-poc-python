import React , { useState, useEffect }from 'react'
import PaymentItemSummary from "./PaymentItemSummary";
import { PaymentItemService } from '../services/PaymentItemService'
// import NewPagination from "./NewPagination";
import { useNavigate } from 'react-router-dom';
// import ConfirmModal from "./ConfirmModal";

// import { Row, Col, Spinner } from 'react-bootstrap';

const Spinner = ({animation}) => {
    return (
        <div className={`spinner-border ${animation ? 'spinner-border-sm' : ''}`} role="status">
            <span className="sr-only">Loading...</span>
        </div>
    )
};

const PaymentItemList = ({useStore}) => {

    let navigate = useNavigate();

    const [loading, setLoading] = useState(true);
    const [paymentItems, setPaymentItems] = useState([]);
    const [currentPage, setCurrentPage] = useState({page:1, page_size:5});
    const [currentPageMeta, setCurrentPageMeta] = useState({total_items_count:5, current_page_number:1, total_pages_count:1});

    const [showModal, setShowModal] = useState(false);
    const [deleteId, setDeleteId] = useState();

    useEffect(() => {
        fetchPaymentItems(currentPage);
    },[currentPage]);
    
    let fetchPaymentItems = (pageInfo) => {
        setLoading(true);
        // PaymentItemService.getPaymentItemsPaged(pageInfo).then(res => {
        //     setPaymentItems(res.data.paymentItems);
        //     setCurrentPageMeta(pageInfo);
        //     setCurrentPageMeta(res.data.page_meta);
        //     setLoading(false);
        // }).catch(err => {      
        //     console.error(err);
        // });       
    };


    let deletePaymentItem = (id) => {
        setDeleteId(id);
        setShowModal(true);
    }

    let handleConfirmDelete = () => {
        PaymentItemService.deletePaymentItem(deleteId)
        .then(res => {
            fetchPaymentItems(currentPage);
            navigate('/items');
        })
        .catch(err => {
            console.error(err);
        });
        setShowModal(false);
    }

    const handlePageChange = (e) => {
        setCurrentPage({page: 1, page_size: parseInt(e)});
    }
    

    const listItems = paymentItems.map((paymentItem) => (
        <div className="p-2 m-1 bg-white rounded" key={paymentItem.id}>  
            <PaymentItemSummary
                useStore={useStore}
                handleDeleteCallback={deletePaymentItem}
                paymentItem={paymentItem}/>       
        </div>    
    ));

    return (<>

        <div>
            {loading && <Spinner animation='border' />}
            {paymentItems.length>0 ? 
            <>
            <div className='grid grid-cols-1 sm:grid-cols-2 md:grid-cols-2 lg:grid-cols-3 xl:grid-cols-4'>
                {listItems}
            </div>
            {currentPage && <div className='mb-5'><NewPagination pageInfo={currentPage} pageMeta={currentPageMeta} handlePageChange={handlePageChange} fetchPage={setCurrentPage}/></div>}
            <ConfirmModal showModal={showModal} actionName={'Delete PaymentItem'} actionDescription={'delete this paymentItem'} actionCallback={handleConfirmDelete}/>
            </>

            : 
            <div>No Payment Items</div>}
        </div>

    </>);
};

export default PaymentItemList;

