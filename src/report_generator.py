from datetime import datetime, timedelta
from typing import List, Dict, Any
import json
from pathlib import Path
from data_sources.nasa_connector import NASADataConnector, SatelliteData
from crewai import Agent, Task, Crew, Process
import logging

class ReportGenerator:
    """Generates the Geoengineering Weekly Intelligence Report"""
    
    def __init__(self):
        self.nasa_connector = NASADataConnector()
        self.report_template = {
            "title": "Geoengineering Weekly Intelligence Report",
            "date": "",
            "version": "v1.2",
            "data_sources": [],
            "executive_summary": "",
            "key_data_updates": {},
            "new_developments": [],
            "action_items": [],
            "references": [],
            "next_update": ""
        }
        
    def create_analysis_crew(self) -> Crew:
        """Create a crew of AI agents for report analysis"""
        
        data_analyst = Agent(
            role="Climate Data Analyst",
            goal="Analyze climate data for significant patterns and changes",
            backstory="Expert in climate data analysis with focus on satellite observations"
        )
        
        research_analyst = Agent(
            role="Research Analyst",
            goal="Identify and analyze new developments in geoengineering",
            backstory="Specialized in tracking and analyzing geoengineering research and policy"
        )
        
        report_writer = Agent(
            role="Report Writer",
            goal="Synthesize findings into clear, actionable intelligence",
            backstory="Experienced in creating comprehensive intelligence reports"
        )
        
        return Crew(
            agents=[data_analyst, research_analyst, report_writer],
            tasks=[
                Task(
                    description="Analyze satellite data for patterns and anomalies",
                    agent=data_analyst
                ),
                Task(
                    description="Research and summarize new geoengineering developments",
                    agent=research_analyst
                ),
                Task(
                    description="Create comprehensive intelligence report",
                    agent=report_writer
                )
            ],
            process=Process.sequential
        )

    def analyze_satellite_data(self, data: List[SatelliteData]) -> Dict[str, Any]:
        """
        Analyze the satellite data for patterns and insights
        
        Args:
            data: List of SatelliteData objects
            
        Returns:
            Dictionary containing analysis results
        """
        if not data:
            return {
                "status": "No data available",
                "insights": [],
                "recommendations": []
            }
            
        # Create analysis crew
        crew = self.create_analysis_crew()
        
        # Prepare data for analysis
        analysis_data = {
            "raw_data": [d.dict() for d in data],
            "time_range": {
                "start": min(d.timestamp for d in data),
                "end": max(d.timestamp for d in data)
            }
        }
        
        # Run the crew's analysis
        result = crew.run(analysis_data)
        return result

    def generate_report(self) -> Dict[str, Any]:
        """
        Generate the weekly intelligence report
        
        Returns:
            Dictionary containing the complete report
        """
        # Initialize report with current date
        report = self.report_template.copy()
        current_time = datetime.now()
        report["date"] = current_time.strftime("%Y-%m-%d")
        
        # Collect data from sources
        satellite_data = self.nasa_connector.get_latest_data()
        
        # Record data sources and their timestamps
        report["data_sources"] = [{
            "name": "NASA Cloud Radar System",
            "last_updated": current_time.isoformat(),
            "status": "Active" if satellite_data else "No Data Available"
        }]
        
        # Analyze data and generate insights
        analysis_results = self.analyze_satellite_data(satellite_data)
        
        # Update report sections
        report["executive_summary"] = analysis_results.get("executive_summary", "No summary available")
        report["key_data_updates"] = {
            "satellite_observations": analysis_results.get("satellite_analysis", {}),
        }
        report["new_developments"] = analysis_results.get("developments", [])
        report["action_items"] = analysis_results.get("recommendations", [])
        report["references"] = self._generate_references(analysis_results)
        
        # Set next update date
        next_update = current_time + timedelta(days=7)
        report["next_update"] = next_update.strftime("%Y-%m-%d")
        
        return report
    
    def save_report(self, report: Dict[str, Any], output_dir: str = "reports") -> str:
        """
        Save the report to a file
        
        Args:
            report: Report dictionary
            output_dir: Directory to save the report
            
        Returns:
            Path to the saved report file
        """
        # Create output directory if it doesn't exist
        Path(output_dir).mkdir(parents=True, exist_ok=True)
        
        # Generate filename with timestamp
        filename = f"geoengineering_report_{report['date']}.json"
        filepath = Path(output_dir) / filename
        
        # Save report as JSON
        with open(filepath, 'w') as f:
            json.dump(report, f, indent=2)
            
        logging.info(f"Report saved to {filepath}")
        return str(filepath)
    
    def _generate_references(self, analysis_results: Dict[str, Any]) -> List[str]:
        """Generate references from analysis results"""
        references = []
        
        # Add data source references
        references.append("NASA Earth Data: https://www.earthdata.nasa.gov/")
        
        # Add any additional references from analysis
        if "references" in analysis_results:
            references.extend(analysis_results["references"])
            
        return references 