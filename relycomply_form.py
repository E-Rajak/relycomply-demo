import streamlit as st
from data_models import CustomerType, IDDocumentType, Customer, DocumentType, Document
from utils import generate_hash, match_input_for_enum, encode_image_to_base64
import pycountry
from dataclasses import asdict
from relycomply_client import RelyComplyGQLClient
from dotenv import load_dotenv

load_dotenv()
client = RelyComplyGQLClient()

customer_tab, document_tab = st.tabs(["Create Customer", "Create Document"])

# First tab with a form
with customer_tab:
    st.header("Create customer")
    with st.form("customer_form"):
        type = st.selectbox('Customer Type', [cust.value for cust in CustomerType])
        firstName = st.text_input('First Name')
        middleName = st.text_input('Middle Name')
        lastName = st.text_input('Last Name')
        idDocumentType = st.selectbox(
            'ID Document Type', [doc.value for doc in IDDocumentType]
        )
        idDocumentCode = st.text_input('ID Document Code')
        nationality = st.selectbox('Nationality', [c.name for c in pycountry.countries])
        residence = st.selectbox('Residence', [c.name for c in pycountry.countries])
        birthdate = st.date_input('Date of Birth')

        submitted = st.form_submit_button('Create')
        if submitted:
            identifier = generate_hash(first_name=firstName, id_number=idDocumentCode)
            customer = Customer(
                identifier=identifier,
                type=match_input_for_enum(type, CustomerType),
                firstName=firstName,
                middleName=middleName,
                lastName=lastName,
                idDocumentType=match_input_for_enum(idDocumentType, IDDocumentType),
                idDocumentCode=idDocumentCode,
                nationality=pycountry.countries.get(name=nationality).alpha_2,
                residence=pycountry.countries.get(name=residence).alpha_2,
                birthdate=birthdate.strftime('%Y-%m-%d'),
            )
            result = client.createCustomer(**asdict(customer))
            if result:
                st.write('Created customer with the following details', result)


# Second tab with a different form
with document_tab:
    st.header("Create Document")
    with st.form("document_form"):
        customers = client.customers()
        id_names = [
            f"{customer['id']} - {customer['firstName']} {customer['lastName']}"
            for customer in customers
        ]
        chosen_customer = st.selectbox('Customer', id_names)
        document_type = st.selectbox(
            'Document Type', [doc.value for doc in DocumentType]
        )
        doc = st.file_uploader("Upload a Document", type=["jpg", "jpeg", "png", "pdf"])
        submitted = st.form_submit_button('Create')
        if submitted:
            doc = Document(
                data=encode_image_to_base64(doc),
                customer=chosen_customer.split('-')[0].lstrip(),
                documentType=match_input_for_enum(document_type, DocumentType),
            )
            result = client.createDocument(**asdict(doc))
            if result:
                st.write('Created document with the following details', result)
