from dataclasses import dataclass
from enum import Enum


class CustomerType(Enum):
    individual = 'Individual'
    organisation = 'Organisation'


class IDDocumentType(Enum):
    entity_registration = 'Entity registration documents'
    za_id_card = 'ZA smart ID card'
    za_id_greenbook = 'ZA green ID book'
    passport = 'Passport'
    za_asylum_paper = 'ZA asylum seeker papers'
    za_refugee_book = 'ZA refugee book'
    generic_id = 'ZA refugee book'


class DocumentType(Enum):
    face_photo = 'Selfie'
    za_id_card_front = 'Font of smart ZA ID card'
    za_id_card_back = 'Back of smart ZA ID card'
    za_id_greenbook = 'ZA ID book'
    passport = 'Passport'
    za_refugee_book = 'ZA refugee book'
    za_asylum_paper = 'ZA asylum papers'
    proof_of_address = 'Proof of address'
    proof_of_source_of_funds = 'Proof of source of funds'


@dataclass
class Customer:
    identifier: str
    type: CustomerType
    firstName: str
    middleName: str
    lastName: str
    idDocumentType: IDDocumentType
    idDocumentCode: str
    nationality: str
    residence: str
    birthdate: str


@dataclass
class Document:
    data: str
    customer: str
    documentType: DocumentType
