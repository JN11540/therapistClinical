from sqlalchemy import Column, Integer, Float, String, Boolean, ForeignKey

from model.base import Base


class ObjectiveMeasurement(Base):
    id             = Column(Integer, primary_key=True, autoincrement=True)
    measurement_id = Column(Integer, ForeignKey("measurement.id"), nullable=False)
    side           = Column(Integer, nullable=False)
    vas_before_test          = Column(Integer, nullable=True)
    vas_after_test           = Column(Integer, nullable=True)
    tug_time_seconds         = Column(Float,   nullable=False)
    tug_assistive_device     = Column(Boolean, nullable=True)
    tug_comment              = Column(String,  nullable=True)
    ftsst_time_seconds       = Column(Float,   nullable=False)
    ftsst_assistive_device   = Column(Boolean, nullable=True)
    ftsst_comment            = Column(String,  nullable=True)
    mwt_10_time_seconds      = Column(Float,   nullable=False)
    mwt_10_assistive_device  = Column(Boolean, nullable=True)
    mwt_10_comment           = Column(String,  nullable=True)
    sls_time_seconds         = Column(Float,   nullable=False)
    sls_comment              = Column(String,  nullable=True)
    rom_knee_flexion_min     = Column(Integer, nullable=False)
    rom_knee_flexion_max     = Column(Integer, nullable=False)
    rom_knee_flexion_comment = Column(String,  nullable=True)
    rom_knee_extension_min   = Column(Integer, nullable=True)
    rom_knee_extension_max   = Column(Integer, nullable=True)
    rom_knee_extension_comment = Column(String, nullable=True)
    mmt_knee_flexion         = Column(Integer, nullable=False)
    mmt_knee_extension       = Column(Integer, nullable=False)
    thigh_circumference      = Column(Float,   nullable=True)
