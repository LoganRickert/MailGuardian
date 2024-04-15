import React, { useEffect, useState } from 'react';
import axios from 'axios';
import DOMPurify from 'dompurify';

function EmailList({ emailFilter }) {
    const [emails, setEmails] = useState([]);
    const [selectedEmail, setSelectedEmail] = useState(null);

    useEffect(() => {
        if (!emailFilter) return;  // Prevent fetching if no emailFilter is selected

        const fetchData = async () => {
            try {
                const response = await axios.post(`${process.env.REACT_APP_API_URL}/api/v1/emails`, {
                    email_filter: emailFilter,
                    limit: 10
                }, {
                    headers: {
                        Authorization: `Bearer ${localStorage.getItem('access_token')}`
                    }
                });
                setEmails(response.data.emails);
            } catch (error) {
                console.error('Failed to fetch emails:', error);
            }
        };

        fetchData();
    }, [emailFilter]);  // Dependency array ensures fetchData runs when emailFilter changes

    const handleSelectEmail = (email) => {
        setSelectedEmail(email);
    };

    const handleStarEmail = async (emailUuid) => {
        console.log("Star email:", emailUuid);
    };

    const handleDeleteEmail = async (emailUuid) => {
        console.log("Delete email:", emailUuid);
    };

    const createMarkup = (htmlContent) => {
        return {__html: DOMPurify.sanitize(htmlContent)};
    };

    return (
        <div className="d-flex" style={{ height: '100%' }}>
            <div className="email-list overflow-auto" style={{ width: selectedEmail ? '50%' : '100%' }}>
                {emails.map(email => (
                    <div key={email.email_uuid} 
                        className="list-group-item list-group-item-action d-flex justify-content-between align-items-center"
                        onClick={() => handleSelectEmail(email)}>
                        <div>
                            <strong>{email.subject}</strong>
                            <br />
                            <small className="text-muted">{email.from}</small>
                        </div>
                        <div>
                            <button className="btn btn-sm btn-outline-primary" onClick={(e) => {e.stopPropagation(); handleStarEmail(email.email_uuid);}}>Star</button>
                            <button className="btn btn-sm btn-outline-danger" onClick={(e) => {e.stopPropagation(); handleDeleteEmail(email.email_uuid);}}>Delete</button>
                        </div>
                    </div>
                ))}
            </div>
            {selectedEmail && (
            <div className="email-preview w-50 p-3" style={{ borderLeft: '2px solid #ccc', position: 'relative' }}>
                <div style={{ position: 'absolute', top: 0, right: 10 }}>
                    <button className="btn btn-sm btn-outline-secondary" onClick={() => setSelectedEmail(null)}>Close</button>
                    <button className="btn btn-sm btn-outline-primary">Reply</button>
                    <button className="btn btn-sm btn-outline-primary">Reply All</button>
                </div>
                <div className="p-3">
                    <h3>{selectedEmail.subject}</h3>
                    <h5>From: {selectedEmail.from}</h5>
                    <h6>To: {selectedEmail.to}</h6>
                    <div><strong>Received At:</strong> {new Date(selectedEmail.received_at).toLocaleString()}</div>
                    <div className="html-content mt-2" dangerouslySetInnerHTML={createMarkup(selectedEmail.html || selectedEmail.text)}></div>
                    <div>
                        <strong>Attachments:</strong>
                        {selectedEmail.attachments.map(att => (
                            <div key={att.file_uuid}>{att.file_name} - <a href={att.file_path}>Download</a></div>
                        ))}
                    </div>
                </div>
            </div>
            )}
        </div>
    );
}

export default EmailList;
