import os
import pandas as pd
import numpy as np
import h5py
from datetime import datetime, timedelta
from typing import Dict, List, Optional
from pydantic import BaseModel
import logging
from pathlib import Path

class SatelliteData(BaseModel):
    timestamp: datetime
    reflectivity: float
    doppler_velocity: Optional[float]
    location: Dict[str, float]
    source: str
    metadata: Dict[str, str]

class NASADataConnector:
    """Connector for NASA CRS (Cloud Radar System) Data"""
    
    def __init__(self, data_dir: Optional[str] = None):
        self.data_dir = data_dir or os.path.join(os.getcwd(), 'data', 'crs')
        os.makedirs(self.data_dir, exist_ok=True)
        
    def get_cloud_radar_data(self, start_date: datetime, end_date: datetime) -> List[SatelliteData]:
        """
        Read CRS reflectivity and Doppler velocity data
        
        Args:
            start_date: Start date for data collection
            end_date: End date for data collection
            
        Returns:
            List of SatelliteData objects containing the measurements
        """
        try:
            # List available HDF5 files in the directory
            data_files = [f for f in os.listdir(self.data_dir) if f.endswith('.h5')]
            
            if not data_files:
                logging.warning(f"No CRS HDF5 files found in {self.data_dir}")
                return []
                
            results = []
            for file in data_files:
                file_date = self._parse_date_from_filename(file)
                if start_date <= file_date <= end_date:
                    data = self._read_crs_file(os.path.join(self.data_dir, file))
                    results.extend(data)
            
            return results
            
        except Exception as e:
            logging.error(f"Error reading CRS data: {str(e)}")
            return []

    def get_latest_data(self) -> List[SatelliteData]:
        """
        Get the most recent week of data
        
        Returns:
            List of SatelliteData objects from the past week
        """
        end_date = datetime.now()
        start_date = end_date - timedelta(days=7)
        return self.get_cloud_radar_data(start_date, end_date)

    def _parse_date_from_filename(self, filename: str) -> datetime:
        """Extract date from CRS filename format"""
        # Example filename format: IMPACTS_CRS_L1B_YYYYMMDD_[flight_number].h5
        date_str = filename.split('_')[3]
        return datetime.strptime(date_str, '%Y%m%d')

    def _read_crs_file(self, filepath: str) -> List[SatelliteData]:
        """
        Read and parse CRS HDF5 file for IMPACTS campaign
        
        The IMPACTS CRS HDF5 files contain:
        - Time/Data/TimeUTC: Time in seconds since epoch (1970-01-01)
        - Products/Information/Range: Range/height values (m)
        - Products/Data/dBZe: Radar Reflectivity (dBZ)
        - Products/Data/Velocity_corrected: Doppler Velocity (m/s)
        """
        try:
            results = []
            t0 = datetime.fromisoformat('1970-01-01T00:00:00')  # Epoch time reference
            
            with h5py.File(filepath, 'r') as f:
                # Get metadata
                metadata = self._extract_hdf5_metadata(f)
                
                # Get datasets using correct paths
                time_utc = f['Time']['Data']['TimeUTC'][:]  # seconds since epoch
                range_data = f['Products']['Information']['Range'][:] / 1000.0  # Convert from m to km
                dbz = f['Products']['Data']['dBZe'][:]  # Reflectivity
                velocity = f['Products']['Data']['Velocity_corrected'][:]  # Corrected Doppler velocity
                
                # Convert times to datetime objects
                times = [t0 + timedelta(seconds=float(s)) for s in time_utc]
                
                # Process each time step
                for i, timestamp in enumerate(times):
                    # Process each range bin
                    for j, height in enumerate(range_data):
                        results.append(
                            SatelliteData(
                                timestamp=timestamp,
                                reflectivity=float(dbz[i, j]),
                                doppler_velocity=float(velocity[i, j]) if velocity is not None else None,
                                location={
                                    'height': float(height),
                                    'latitude': metadata.get('latitude', 0.0),
                                    'longitude': metadata.get('longitude', 0.0)
                                },
                                source='NASA Cloud Radar System (CRS)',
                                metadata={
                                    'instrument': 'CRS',
                                    'processing_level': metadata.get('processing_level', 'L1B'),
                                    'quality': metadata.get('quality', 'Good'),
                                    'flight_info': metadata.get('flight_info', '')
                                }
                            )
                        )
            return results
            
        except Exception as e:
            logging.error(f"Error parsing CRS file {filepath}: {str(e)}")
            logging.error(f"File structure: {self._print_hdf5_structure(filepath)}")
            return []
            
    def _print_hdf5_structure(self, filepath: str) -> str:
        """Helper function to print HDF5 file structure for debugging"""
        structure = []
        
        def _print_attrs(name, obj):
            if isinstance(obj, h5py.Dataset):
                structure.append(f"Dataset: {name}, Shape: {obj.shape}, Type: {obj.dtype}")
            elif isinstance(obj, h5py.Group):
                structure.append(f"Group: {name}")
        
        with h5py.File(filepath, 'r') as f:
            f.visititems(_print_attrs)
            
        return "\n".join(structure)

    def _extract_hdf5_metadata(self, h5file: h5py.File) -> Dict[str, Any]:
        """Extract metadata from HDF5 file attributes"""
        metadata = {}
        
        try:
            # Get global attributes
            for attr_name, attr_value in h5file.attrs.items():
                if isinstance(attr_value, bytes):
                    attr_value = attr_value.decode('utf-8')
                metadata[attr_name.lower()] = attr_value
                
            # Try to get specific metadata fields
            if 'FlightDate' in h5file.attrs:
                date_str = h5file.attrs['FlightDate'].decode('utf-8')
                metadata['date'] = datetime.strptime(date_str, '%Y-%m-%d').date()
                
            if 'Aircraft' in h5file.attrs:
                metadata['flight_info'] = h5file.attrs['Aircraft'].decode('utf-8')
                
            if 'ProcessingLevel' in h5file.attrs:
                metadata['processing_level'] = h5file.attrs['ProcessingLevel'].decode('utf-8')
                
            if 'Quality' in h5file.attrs:
                metadata['quality'] = h5file.attrs['Quality'].decode('utf-8')
                
        except Exception as e:
            logging.warning(f"Error extracting HDF5 metadata: {str(e)}")
            
        return metadata

    def download_sample_data(self):
        """
        Download sample CRS data files for testing
        This would typically connect to NASA's data distribution servers
        """
        # TODO: Implement data download from NASA GHRC DAAC
        pass 