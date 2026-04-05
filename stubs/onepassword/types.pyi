from _typeshed import Incomplete
from datetime import datetime
from enum import Enum
from pydantic import BaseModel, BeforeValidator as BeforeValidator, PlainSerializer as PlainSerializer
from typing import Annotated, Generic, Literal, TypeVar

E = TypeVar('E')
T = TypeVar('T')

def serialize_binary_data(value: bytes) -> list[int]: ...
def deserialize_binary_data(value): ...
def serialize_datetime_data(utc_time: datetime) -> str: ...
def parse_rfc3339(date_str: str) -> datetime: ...
ErrorMessage = str

class AddressFieldDetails(BaseModel):
    street: str
    city: str
    country: str
    zip: str
    state: str

class DocumentCreateParams(BaseModel):
    name: str
    content: Annotated[bytes, None, None]

class FileAttributes(BaseModel):
    name: str
    id: str
    size: int

class FileCreateParams(BaseModel):
    model_config: Incomplete
    name: str
    content: Annotated[bytes, None, None]
    section_id: str
    field_id: str

class GeneratePasswordResponse(BaseModel):
    password: str

class GroupType(str, Enum):
    OWNERS = 'owners'
    ADMINISTRATORS = 'administrators'
    RECOVERY = 'recovery'
    EXTERNALACCOUNTMANAGERS = 'externalAccountManagers'
    TEAMMEMBERS = 'teamMembers'
    USERDEFINED = 'userDefined'
    UNSUPPORTED = 'unsupported'

class GroupState(str, Enum):
    ACTIVE = 'active'
    DELETED = 'deleted'
    UNSUPPORTED = 'unsupported'

class VaultAccessorType(str, Enum):
    USER = 'user'
    GROUP = 'group'

class VaultAccess(BaseModel):
    model_config: Incomplete
    vault_uuid: str
    accessor_type: VaultAccessorType
    accessor_uuid: str
    permissions: int

class Group(BaseModel):
    model_config: Incomplete
    id: str
    title: str
    description: str
    group_type: GroupType
    state: GroupState
    vault_access: list[VaultAccess] | None

class GroupAccess(BaseModel):
    model_config: Incomplete
    group_id: str
    permissions: int

class GroupGetParams(BaseModel):
    model_config: Incomplete
    vault_permissions: bool | None

class GroupVaultAccess(BaseModel):
    model_config: Incomplete
    vault_id: str
    group_id: str
    permissions: int

class ItemCategory(str, Enum):
    LOGIN = 'Login'
    SECURENOTE = 'SecureNote'
    CREDITCARD = 'CreditCard'
    CRYPTOWALLET = 'CryptoWallet'
    IDENTITY = 'Identity'
    PASSWORD = 'Password'
    DOCUMENT = 'Document'
    APICREDENTIALS = 'ApiCredentials'
    BANKACCOUNT = 'BankAccount'
    DATABASE = 'Database'
    DRIVERLICENSE = 'DriverLicense'
    EMAIL = 'Email'
    MEDICALRECORD = 'MedicalRecord'
    MEMBERSHIP = 'Membership'
    OUTDOORLICENSE = 'OutdoorLicense'
    PASSPORT = 'Passport'
    REWARDS = 'Rewards'
    ROUTER = 'Router'
    SERVER = 'Server'
    SSHKEY = 'SshKey'
    SOCIALSECURITYNUMBER = 'SocialSecurityNumber'
    SOFTWARELICENSE = 'SoftwareLicense'
    PERSON = 'Person'
    UNSUPPORTED = 'Unsupported'

class ItemFieldType(str, Enum):
    TEXT = 'Text'
    CONCEALED = 'Concealed'
    CREDITCARDTYPE = 'CreditCardType'
    CREDITCARDNUMBER = 'CreditCardNumber'
    PHONE = 'Phone'
    URL = 'Url'
    TOTP = 'Totp'
    EMAIL = 'Email'
    REFERENCE = 'Reference'
    SSHKEY = 'SshKey'
    MENU = 'Menu'
    MONTHYEAR = 'MonthYear'
    ADDRESS = 'Address'
    DATE = 'Date'
    UNSUPPORTED = 'Unsupported'

class ItemFieldDetailsTypes(str, Enum):
    OTP = 'Otp'
    SSH_KEY = 'SshKey'
    ADDRESS = 'Address'

class ItemFieldDetailsOtp(BaseModel):
    type: Literal[ItemFieldDetailsTypes.OTP]
    content: OtpFieldDetails

class ItemFieldDetailsSshKey(BaseModel):
    type: Literal[ItemFieldDetailsTypes.SSH_KEY]
    content: SshKeyAttributes | None

class ItemFieldDetailsAddress(BaseModel):
    type: Literal[ItemFieldDetailsTypes.ADDRESS]
    content: AddressFieldDetails | None
ItemFieldDetails = ItemFieldDetailsOtp | ItemFieldDetailsSshKey | ItemFieldDetailsAddress

class ItemField(BaseModel):
    model_config: Incomplete
    id: str
    title: str
    section_id: str | None
    field_type: ItemFieldType
    value: str
    details: ItemFieldDetails | None

class ItemSection(BaseModel):
    id: str
    title: str

class AutofillBehavior(str, Enum):
    ANYWHEREONWEBSITE = 'AnywhereOnWebsite'
    EXACTDOMAIN = 'ExactDomain'
    NEVER = 'Never'

class Website(BaseModel):
    model_config: Incomplete
    url: str
    label: str
    autofill_behavior: AutofillBehavior

class ItemFile(BaseModel):
    model_config: Incomplete
    attributes: FileAttributes
    section_id: str
    field_id: str

class Item(BaseModel):
    model_config: Incomplete
    id: str
    title: str
    category: ItemCategory
    vault_id: str
    fields: list[ItemField]
    sections: list[ItemSection]
    notes: str
    tags: list[str]
    websites: list[Website]
    version: int
    files: list[ItemFile]
    document: FileAttributes | None
    created_at: Annotated[datetime, None, None]
    updated_at: Annotated[datetime, None, None]

class ItemCreateParams(BaseModel):
    model_config: Incomplete
    category: ItemCategory
    vault_id: str
    title: str
    fields: list[ItemField] | None
    sections: list[ItemSection] | None
    notes: str | None
    tags: list[str] | None
    websites: list[Website] | None
    files: list[FileCreateParams] | None
    document: DocumentCreateParams | None

class ItemState(str, Enum):
    ACTIVE = 'active'
    ARCHIVED = 'archived'

class ItemOverview(BaseModel):
    model_config: Incomplete
    id: str
    title: str
    category: ItemCategory
    vault_id: str
    websites: list[Website]
    tags: list[str]
    created_at: Annotated[datetime, None, None]
    updated_at: Annotated[datetime, None, None]
    state: ItemState

class ItemShareDuration(str, Enum):
    ONEHOUR = 'OneHour'
    ONEDAY = 'OneDay'
    SEVENDAYS = 'SevenDays'
    FOURTEENDAYS = 'FourteenDays'
    THIRTYDAYS = 'ThirtyDays'

class AllowedType(str, Enum):
    AUTHENTICATED = 'Authenticated'
    PUBLIC = 'Public'

class AllowedRecipientType(str, Enum):
    EMAIL = 'Email'
    DOMAIN = 'Domain'

class ItemShareFiles(BaseModel):
    model_config: Incomplete
    allowed: bool
    max_size: int
    allowed_types: list[AllowedType] | None
    allowed_recipient_types: list[AllowedRecipientType] | None
    max_expiry: ItemShareDuration | None
    default_expiry: ItemShareDuration | None
    max_views: int | None

class ItemShareAccountPolicy(BaseModel):
    model_config: Incomplete
    max_expiry: ItemShareDuration
    default_expiry: ItemShareDuration
    max_views: int | None
    allowed_types: list[AllowedType]
    allowed_recipient_types: list[AllowedRecipientType]
    files: ItemShareFiles

class ValidRecipientEmailInner(BaseModel):
    email: str

class ValidRecipientDomainInner(BaseModel):
    domain: str

class ValidRecipientTypes(str, Enum):
    EMAIL = 'Email'
    DOMAIN = 'Domain'

class ValidRecipientEmail(BaseModel):
    type: Literal[ValidRecipientTypes.EMAIL]
    parameters: ValidRecipientEmailInner

class ValidRecipientDomain(BaseModel):
    type: Literal[ValidRecipientTypes.DOMAIN]
    parameters: ValidRecipientDomainInner
ValidRecipient = ValidRecipientEmail | ValidRecipientDomain

class ItemShareParams(BaseModel):
    model_config: Incomplete
    recipients: list[ValidRecipient] | None
    expire_after: ItemShareDuration | None
    one_time_only: bool

class Response(BaseModel, Generic[T, E]):
    content: T | None
    error: E | None

class ItemUpdateFailureReasonTypes(str, Enum):
    ITEM_VALIDATION_ERROR = 'itemValidationError'
    ITEM_STATUS_PERMISSION_ERROR = 'itemStatusPermissionError'
    ITEM_STATUS_INCORRECT_ITEM_VERSION = 'itemStatusIncorrectItemVersion'
    ITEM_STATUS_FILE_NOT_FOUND = 'itemStatusFileNotFound'
    ITEM_STATUS_TOO_BIG = 'itemStatusTooBig'
    ITEM_NOT_FOUND = 'itemNotFound'
    INTERNAL = 'internal'

class ItemUpdateFailureReasonItemValidationError(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.ITEM_VALIDATION_ERROR]
    message: ErrorMessage

class ItemUpdateFailureReasonItemStatusPermissionError(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.ITEM_STATUS_PERMISSION_ERROR]

class ItemUpdateFailureReasonItemStatusIncorrectItemVersion(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.ITEM_STATUS_INCORRECT_ITEM_VERSION]

class ItemUpdateFailureReasonItemStatusFileNotFound(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.ITEM_STATUS_FILE_NOT_FOUND]

class ItemUpdateFailureReasonItemStatusTooBig(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.ITEM_STATUS_TOO_BIG]

class ItemUpdateFailureReasonItemNotFound(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.ITEM_NOT_FOUND]

class ItemUpdateFailureReasonInternal(BaseModel):
    type: Literal[ItemUpdateFailureReasonTypes.INTERNAL]
    message: ErrorMessage
ItemUpdateFailureReason = ItemUpdateFailureReasonItemValidationError | ItemUpdateFailureReasonItemStatusPermissionError | ItemUpdateFailureReasonItemStatusIncorrectItemVersion | ItemUpdateFailureReasonItemStatusFileNotFound | ItemUpdateFailureReasonItemStatusTooBig | ItemUpdateFailureReasonItemNotFound | ItemUpdateFailureReasonInternal

class ItemsDeleteAllResponse(BaseModel):
    model_config: Incomplete
    individual_responses: dict[str, Response[None, ItemUpdateFailureReason]]

class ItemsGetAllErrorTypes(str, Enum):
    ITEM_NOT_FOUND = 'itemNotFound'
    INTERNAL = 'internal'

class ItemsGetAllErrorItemNotFound(BaseModel):
    type: Literal[ItemsGetAllErrorTypes.ITEM_NOT_FOUND]

class ItemsGetAllErrorInternal(BaseModel):
    type: Literal[ItemsGetAllErrorTypes.INTERNAL]
    message: ErrorMessage
ItemsGetAllError = ItemsGetAllErrorItemNotFound | ItemsGetAllErrorInternal

class ItemsGetAllResponse(BaseModel):
    model_config: Incomplete
    individual_responses: list[Response[Item, ItemsGetAllError]]

class ItemsUpdateAllResponse(BaseModel):
    model_config: Incomplete
    individual_responses: list[Response[Item, ItemUpdateFailureReason]]

class OtpFieldDetails(BaseModel):
    model_config: Incomplete
    code: str | None
    error_message: str | None

class ResolvedReference(BaseModel):
    model_config: Incomplete
    secret: str
    item_id: str
    vault_id: str

class ResolveReferenceErrorTypes(str, Enum):
    PARSING = 'parsing'
    FIELD_NOT_FOUND = 'fieldNotFound'
    VAULT_NOT_FOUND = 'vaultNotFound'
    TOO_MANY_VAULTS = 'tooManyVaults'
    ITEM_NOT_FOUND = 'itemNotFound'
    TOO_MANY_ITEMS = 'tooManyItems'
    TOO_MANY_MATCHING_FIELDS = 'tooManyMatchingFields'
    NO_MATCHING_SECTIONS = 'noMatchingSections'
    INCOMPATIBLE_TOTP_QUERY_PARAMETER_FIELD = 'incompatibleTOTPQueryParameterField'
    UNABLE_TO_GENERATE_TOTP_CODE = 'unableToGenerateTotpCode'
    S_SH_KEY_METADATA_NOT_FOUND = 'sSHKeyMetadataNotFound'
    UNSUPPORTED_FILE_FORMAT = 'unsupportedFileFormat'
    INCOMPATIBLE_SSH_KEY_QUERY_PARAMETER_FIELD = 'incompatibleSshKeyQueryParameterField'
    UNABLE_TO_PARSE_PRIVATE_KEY = 'unableToParsePrivateKey'
    UNABLE_TO_FORMAT_PRIVATE_KEY_TO_OPEN_SSH = 'unableToFormatPrivateKeyToOpenSsh'
    OTHER = 'other'

class ResolveReferenceErrorParsing(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.PARSING]
    message: ErrorMessage

class ResolveReferenceErrorFieldNotFound(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.FIELD_NOT_FOUND]

class ResolveReferenceErrorVaultNotFound(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.VAULT_NOT_FOUND]

class ResolveReferenceErrorTooManyVaults(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.TOO_MANY_VAULTS]

class ResolveReferenceErrorItemNotFound(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.ITEM_NOT_FOUND]

class ResolveReferenceErrorTooManyItems(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.TOO_MANY_ITEMS]

class ResolveReferenceErrorTooManyMatchingFields(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.TOO_MANY_MATCHING_FIELDS]

class ResolveReferenceErrorNoMatchingSections(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.NO_MATCHING_SECTIONS]

class ResolveReferenceErrorIncompatibleTOTPQueryParameterField(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.INCOMPATIBLE_TOTP_QUERY_PARAMETER_FIELD]

class ResolveReferenceErrorUnableToGenerateTotpCode(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.UNABLE_TO_GENERATE_TOTP_CODE]
    message: ErrorMessage

class ResolveReferenceErrorSSHKeyMetadataNotFound(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.S_SH_KEY_METADATA_NOT_FOUND]

class ResolveReferenceErrorUnsupportedFileFormat(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.UNSUPPORTED_FILE_FORMAT]

class ResolveReferenceErrorIncompatibleSshKeyQueryParameterField(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.INCOMPATIBLE_SSH_KEY_QUERY_PARAMETER_FIELD]

class ResolveReferenceErrorUnableToParsePrivateKey(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.UNABLE_TO_PARSE_PRIVATE_KEY]

class ResolveReferenceErrorUnableToFormatPrivateKeyToOpenSsh(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.UNABLE_TO_FORMAT_PRIVATE_KEY_TO_OPEN_SSH]

class ResolveReferenceErrorOther(BaseModel):
    type: Literal[ResolveReferenceErrorTypes.OTHER]
ResolveReferenceError = ResolveReferenceErrorParsing | ResolveReferenceErrorFieldNotFound | ResolveReferenceErrorVaultNotFound | ResolveReferenceErrorTooManyVaults | ResolveReferenceErrorItemNotFound | ResolveReferenceErrorTooManyItems | ResolveReferenceErrorTooManyMatchingFields | ResolveReferenceErrorNoMatchingSections | ResolveReferenceErrorIncompatibleTOTPQueryParameterField | ResolveReferenceErrorUnableToGenerateTotpCode | ResolveReferenceErrorSSHKeyMetadataNotFound | ResolveReferenceErrorUnsupportedFileFormat | ResolveReferenceErrorIncompatibleSshKeyQueryParameterField | ResolveReferenceErrorUnableToParsePrivateKey | ResolveReferenceErrorUnableToFormatPrivateKeyToOpenSsh | ResolveReferenceErrorOther

class ResolveAllResponse(BaseModel):
    model_config: Incomplete
    individual_responses: dict[str, Response[ResolvedReference, ResolveReferenceError]]

class SshKeyAttributes(BaseModel):
    model_config: Incomplete
    public_key: str
    fingerprint: str
    key_type: str

class VaultType(str, Enum):
    PERSONAL = 'personal'
    EVERYONE = 'everyone'
    TRANSFER = 'transfer'
    USERCREATED = 'userCreated'
    UNSUPPORTED = 'unsupported'

class Vault(BaseModel):
    model_config: Incomplete
    id: str
    title: str
    description: str
    vault_type: VaultType
    active_item_count: int
    content_version: int
    attribute_version: int
    access: list[VaultAccess] | None

class VaultCreateParams(BaseModel):
    model_config: Incomplete
    title: str
    description: str | None
    allow_admins_access: bool | None

class VaultGetParams(BaseModel):
    accessors: bool | None

class VaultListParams(BaseModel):
    model_config: Incomplete
    decrypt_details: bool | None

class VaultOverview(BaseModel):
    model_config: Incomplete
    id: str
    title: str
    description: str
    vault_type: VaultType
    active_item_count: int
    content_version: int
    attribute_version: int
    created_at: Annotated[datetime, None, None]
    updated_at: Annotated[datetime, None, None]

class VaultUpdateParams(BaseModel):
    title: str | None
    description: str | None

class ItemListFilterByStateInner(BaseModel):
    active: bool
    archived: bool

class ItemListFilterTypes(str, Enum):
    BY_STATE = 'ByState'

class ItemListFilterByState(BaseModel):
    type: Literal[ItemListFilterTypes.BY_STATE]
    content: ItemListFilterByStateInner
ItemListFilter = ItemListFilterByState

class PasswordRecipeMemorableInner(BaseModel):
    model_config: Incomplete
    separator_type: SeparatorType
    capitalize: bool
    word_list_type: WordListType
    word_count: int

class PasswordRecipePinInner(BaseModel):
    length: int

class PasswordRecipeRandomInner(BaseModel):
    model_config: Incomplete
    include_digits: bool
    include_symbols: bool
    length: int

class PasswordRecipeTypes(str, Enum):
    MEMORABLE = 'Memorable'
    PIN = 'Pin'
    RANDOM = 'Random'

class PasswordRecipeMemorable(BaseModel):
    type: Literal[PasswordRecipeTypes.MEMORABLE]
    parameters: PasswordRecipeMemorableInner

class PasswordRecipePin(BaseModel):
    type: Literal[PasswordRecipeTypes.PIN]
    parameters: PasswordRecipePinInner

class PasswordRecipeRandom(BaseModel):
    type: Literal[PasswordRecipeTypes.RANDOM]
    parameters: PasswordRecipeRandomInner
PasswordRecipe = PasswordRecipeMemorable | PasswordRecipePin | PasswordRecipeRandom

class SeparatorType(str, Enum):
    DIGITS = 'digits'
    DIGITSANDSYMBOLS = 'digitsAndSymbols'
    SPACES = 'spaces'
    HYPHENS = 'hyphens'
    UNDERSCORES = 'underscores'
    PERIODS = 'periods'
    COMMAS = 'commas'

class WordListType(str, Enum):
    FULLWORDS = 'fullWords'
    SYLLABLES = 'syllables'
    THREELETTERS = 'threeLetters'

ARCHIVE_ITEMS: int
CREATE_ITEMS: int
DELETE_ITEMS: int
EXPORT_ITEMS: int
IMPORT_ITEMS: int
MANAGE_VAULT: int
NO_ACCESS: int
PRINT_ITEMS: int
READ_ITEMS: int
RECOVER_VAULT: int
REVEAL_ITEM_PASSWORD: int
SEND_ITEMS: int
UPDATE_ITEMS: int
UPDATE_ITEM_HISTORY: int
