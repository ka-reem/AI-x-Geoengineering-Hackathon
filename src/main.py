import os
import logging
from dotenv import load_dotenv
from report_generator import ReportGenerator
from fastapi import FastAPI, HTTPException
from datetime import datetime
import uvicorn

# Load environment variables
load_dotenv()

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)
logger = logging.getLogger(__name__)

# Initialize FastAPI app
app = FastAPI(
    title="Geoengineering Intelligence Agent",
    description="API for generating Geoengineering Weekly Intelligence Reports",
    version="1.2"
)

# Initialize report generator
report_generator = ReportGenerator()

@app.get("/")
async def root():
    """Root endpoint"""
    return {
        "message": "Geoengineering Intelligence Agent API",
        "version": "1.2",
        "status": "active"
    }

@app.post("/generate-report")
async def generate_report():
    """Generate a new intelligence report"""
    try:
        # Generate the report
        report = report_generator.generate_report()
        
        # Save the report
        filepath = report_generator.save_report(report)
        
        return {
            "status": "success",
            "message": "Report generated successfully",
            "report": report,
            "filepath": filepath
        }
    except Exception as e:
        logger.error(f"Error generating report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error generating report: {str(e)}"
        )

@app.get("/reports/latest")
async def get_latest_report():
    """Get the most recent report"""
    try:
        # Get list of reports
        reports_dir = "reports"
        if not os.path.exists(reports_dir):
            return {"status": "no_reports", "message": "No reports generated yet"}
            
        reports = [f for f in os.listdir(reports_dir) if f.endswith('.json')]
        if not reports:
            return {"status": "no_reports", "message": "No reports generated yet"}
            
        # Get the most recent report
        latest_report = max(reports, key=lambda x: os.path.getctime(os.path.join(reports_dir, x)))
        
        # Read and return the report
        with open(os.path.join(reports_dir, latest_report), 'r') as f:
            return {"status": "success", "report": f.read()}
            
    except Exception as e:
        logger.error(f"Error retrieving latest report: {str(e)}")
        raise HTTPException(
            status_code=500,
            detail=f"Error retrieving latest report: {str(e)}"
        )

def main():
    """Main entry point"""
    # Validate environment variables
    if not os.getenv('OPENAI_API_KEY'):
        logger.error("OPENAI_API_KEY not found in environment variables")
        return
    
    # Start the FastAPI server
    uvicorn.run(
        "main:app",
        host="0.0.0.0",
        port=8000,
        reload=True
    )

if __name__ == "__main__":
    main() 