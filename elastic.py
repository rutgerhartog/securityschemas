from pydantic import BaseModel, FileUrl, IPvAnyAddress, validator
from auxiliary.hostname import Hostname
from auxiliary.mac import MACAddress
from auxiliary.port import NetworkPort
from enum import Enum 
from __future__ import annotations
import datetime

class Original(BaseModel):
    original: str 

class Agent(BaseModel):
    build: Original 

class Organization(BaseModel):
    name: str 


class AutonomousSystemFields(BaseModel):
    number: int 
    organization: Organization

    

class IPPortPair(BaseModel):
    ip: IPvAnyAddress
    port: NetworkPort

class Client(BaseModel):
    address: IPvAnyAddress | Hostname
    as_: AutonomousSystemFields 
    bytes: int 
    domain: Hostname 
    geo: Geo 
    ip: IPvAnyAddress
    mac: MACAddress.addr
    nat: IPPortPair 
    packets: int 
    port: NetworkPort 
    registered_domain: Hostname 
    subdomain: str 
    top_level_domain: str 
    user: User 

    @validator('registered_domain')
    def check_registered_domain(cls, v, values) -> None:
        assert v.endswith(values['top_level_domain']), f"The registered domain {v} does not end with the given top level domain {values['top_level_domain']}"

    @validator('domain')
    def check_domain(cls, v, values) -> None:
        assert v.endswith(values['registered_domain']), f"The domain {v} does not ends with the registered domain {values['registered_domain']}"


# class ContinentCode(Enum):
#     AF = "Africa"
#     AN = "Antarctica"
#     AS = "Asia"
#     EU = "Europe"
#     NA = "North America"
#     OC = "Oceania"
#     SA = "South America"

class GeoLocation(BaseModel):
    lon: float 
    lat: float 
    @validator('lon', 'lat')
    def check_boundary(cls, v):
        assert abs(v) <= 180


class Geo(BaseModel):
    """To do : make this better"""
    city_name: str 
    continent_code: str
    continent_name: str
    country_iso_code: str
    country_name: str
    location: GeoLocation
    name: str 
    postal_code: str 
    region_iso_code: str 
    region_name: str 
    timezone: str 


class Group(BaseModel):
    domain: Hostname 
    id: str 
    name: str 

class User(BaseModel):
    changes: User
    domain: Hostname 
    effective: User 
    email: str 
    full_name: str 
    group: Group 
    hash: str 
    name: str 
    id: str 
    roles: list[str]
    target: User

class IDNamePair(BaseModel):
    id: str 
    name: str 

class CloudInstance(BaseModel):
    id: str 
    name: str 
    type: str 

class CloudService(BaseModel):
    name: str

class Cloud(BaseModel):
    account: IDNamePair 
    availability_zone: str  # TODO: improve 
    instance: CloudInstance 
    origin: Cloud 
    project: IDNamePair
    provider: str 
    region: str 
    service: CloudService 
    target: Cloud 

class CloudSignature(BaseModel):
    digest_algorithm: str  # TODO: enum 
    exists: bool 
    signing_id: str 
    status: str 
    subject_name: str 
    team_id: str 
    timestamp: datetime.datetime 
    trusted: bool
    valid: bool  

class CPU(BaseModel):
    usage: int | float  

class Memory(BaseModel):
    usage: int | float 

class BytesObject(BaseModel):
    bytes: int 

class DiskRead(BaseModel):
    bytes: int 

class DiskWrite(BaseModel):
    bytes: int 

class Disk(BaseModel):
    read: DiskRead 
    write: DiskWrite 

class ContainerImage(BaseModel):
    name: str 
    tag: list[str]


class Container(BaseModel):
    cpu: CPU
    disk: Disk
    id: str 
    image: ContainerImage 
    labels: dict 
    memory: Memory
    network: dict[str, int]
    runtime: str 

class DataStreamType(Enum):
    logs = "logs"
    metrics = "metrics"
    traces = "traces"
    synthetics = "synthetics"

class DataStream(BaseModel):
    dataset: str 
    namespace: str 
    type: DataStreamType 
    @validator('namespace')
    def must_comply(cls, v):
        assert v.find('-') < 0
        assert len(v) <= 100

class DLL(BaseModel):
    name: str 
    path: FileUrl

class ElasticCommonSchema(BaseModel): 
    timestamp: datetime.datetime
    labels: dict[str, str] 
    message: str 
    tags: list[str]
    agent: Agent | None
    as_: AutonomousSystemFields | None 
    client: Client | None 
    cloud: Cloud | None 
    # code_signature: CodeSignature | None 
    container: Container | None 
    data_stream: DataStream | None 
    destination: Client | None 

