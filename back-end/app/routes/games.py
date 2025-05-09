from typing import List
from fastapi import APIRouter, status, HTTPException, Depends
import random
from .. import oauth2
from ..schemas import classes_schemas
from ..utils import sqlQuery