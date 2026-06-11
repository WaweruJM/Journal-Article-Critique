from typing import Dict, List
from datetime import datetime
import json

class ReportGenerator:
    def __init__(self, analysis_results: Dict, filename: str):
        self.results = analysis_results
        self.filename = filename
        self.criteria_names = {
            'criterion_1': 'Article Title and Topic Relevance',
            'criterion_2': 'Article Source and Journal Strength',
            'criterion_3': 'Clarity of Research Title (PICO)',
            'criterion_4': 'Authors and Affiliations',
            'criterion_5': 'Abstract as Authentic Summary',
            'criterion_6': 'Introduction and Background',
            'criterion_7': 'Methodology Suitability',
            'criterion_8': 'Results and Their Validity',
            'criterion_9': 'Analysis of Data',
            'criterion_10': 'Discussion of Results',
            'criterion_11': 'Conclusions from Authors',
            'criterion_12': 'Impact of Research Results',
            'criterion_13': 'References and Appropriateness'
        }
    
    def generate_streamlit_html(self) -> str:
        """Generate clean, readable HTML for Streamlit rendering (parsed, not raw)"""
        overall_score = self.results.get('overall_score', 0)
        score_color = self._get_score_color(overall_score)
        score_grade = self._get_grade(overall_score)
        
        html = f'''
        <div style="font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;">
            <!-- Header Score Card -->
            <div style="background: linear-gradient(135deg, #0b3c5d 0%, #1a4a6f 100%); border-radius: 16px; padding: 32px; margin-bottom: 24px; text-align: center; box-shadow: 0 4px 12px rgba(0,0,0,0.1);">
                <h2 style="margin: 0 0 8px 0; color: white; font-size: 24px;">📊 Overall Scientific Quality Score</h2>
                <div style="font-size: 64px; font-weight: bold; color: white; margin: 16px 0;">{overall_score}<span style="font-size: 32px;">/100</span></div>
                <div style="font-size: 20px; color: #3498db; background: rgba(255,255,255,0.15); display: inline-block; padding: 6px 20px; border-radius: 30px; margin-top: 8px;">{score_grade}</div>
                <p style="margin-top: 20px; color: rgba(255,255,255,0.8); font-size: 14px;">📄 {self.filename}</p>
                <p style="margin-top: 4px; color: rgba(255,255,255,0.6); font-size: 12px;">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
            </div>
            
            <!-- Quick Stats Row -->
            <div style="display: grid; grid-template-columns: repeat(3, 1fr); gap: 16px; margin-bottom: 24px;">
                <div style="background: linear-gradient(135deg, #28a745 0%, #20c997 100%); border-radius: 12px; padding: 20px; text-align: center; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <div style="font-size: 36px; font-weight: bold;">{self._count_positives()}</div>
                    <div style="font-size: 14px; margin-top: 8px; opacity: 0.95;">✅ Positive Features</div>
                </div>
                <div style="background: linear-gradient(135deg, #dc3545 0%, #c82333 100%); border-radius: 12px; padding: 20px; text-align: center; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <div style="font-size: 36px; font-weight: bold;">{self._count_omissions()}</div>
                    <div style="font-size: 14px; margin-top: 8px; opacity: 0.95;">⚠️ Areas for Improvement</div>
                </div>
                <div style="background: linear-gradient(135deg, #17a2b8 0%, #138496 100%); border-radius: 12px; padding: 20px; text-align: center; color: white; box-shadow: 0 2px 8px rgba(0,0,0,0.08);">
                    <div style="font-size: 36px; font-weight: bold;">13</div>
                    <div style="font-size: 14px; margin-top: 8px; opacity: 0.95;">📋 Criteria Assessed</div>
                </div>
            </div>
            
            <!-- Executive Summary -->
            <div style="background: #e8f4f8; border-left: 5px solid #3498db; border-radius: 12px; padding: 20px; margin-bottom: 24px; box-shadow: 0 2px 8px rgba(0,0,0,0.05);">
                <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                    <span style="font-size: 20px;">📌</span>
                    <strong style="font-size: 18px; color: #0b3c5d;">Executive Summary</strong>
                </div>
                <p style="color: #2c3e50; line-height: 1.6; margin: 0;">{self._generate_executive_summary()}</p>
            </div>
        '''
        
        # Generate each criterion section
        for i in range(1, 14):
            criterion_key = f'criterion_{i}'
            if criterion_key in self.results:
                html += self._generate_criterion_card(i, self.results[criterion_key])
        
        # Footer
        html += f'''
            <!-- Footer -->
            <div style="text-align: center; padding: 24px; margin-top: 24px; background: #f8f9fa; border-radius: 12px; font-size: 13px; color: #7f8c8d;">
                <p style="margin: 0 0 8px 0;">Critique performed using CASP, STROBE, CONSORT, PRISMA, and SMART reporting guidelines</p>
                <p style="margin: 0;">🔗 <a href="https://wawerujm.github.io" target="_blank" style="color: #3498db; text-decoration: none;">wawerujm.github.io</a> | Evidence-Based Research Platform</p>
            </div>
        </div>
        
        <script>
            // JavaScript for collapsible sections
            function toggleCriterion(element) {{
                const content = element.nextElementSibling;
                const arrow = element.querySelector('.toggle-arrow');
                if (content.style.display === 'none' || content.style.display === '') {{
                    content.style.display = 'block';
                    if (arrow) arrow.innerHTML = '▼';
                }} else {{
                    content.style.display = 'none';
                    if (arrow) arrow.innerHTML = '▶';
                }}
            }}
        </script>
        '''
        
        return html
    
    def _generate_criterion_card(self, num: int, data: Dict) -> str:
        """Generate a single criterion card with collapsible content"""
        score = data.get('score', 0)
        criteria_name = self.criteria_names.get(f'criterion_{num}', f'Criterion {num}')
        
        # Determine color coding based on score
        if score >= 80:
            score_label = "Excellent"
            score_badge_color = "#28a745"
            border_color = "#28a745"
        elif score >= 60:
            score_label = "Satisfactory"
            score_badge_color = "#ffc107"
            border_color = "#ffc107"
        elif score >= 40:
            score_label = "Needs Improvement"
            score_badge_color = "#fd7e14"
            border_color = "#fd7e14"
        else:
            score_label = "Poor"
            score_badge_color = "#dc3545"
            border_color = "#dc3545"
        
        html = f'''
        <div style="border: 1px solid #e0e0e0; border-radius: 12px; margin-bottom: 16px; overflow: hidden; background: white; box-shadow: 0 2px 4px rgba(0,0,0,0.05);">
            <!-- Card Header - Clickable -->
            <div onclick="toggleCriterion(this)" 
                 style="cursor: pointer; background: #fafafa; padding: 16px 20px; border-left: 5px solid {border_color}; display: flex; justify-content: space-between; align-items: center; transition: background 0.2s;">
                <div style="display: flex; align-items: center; gap: 12px; flex-wrap: wrap;">
                    <span style="font-weight: bold; font-size: 18px; color: #2c3e50;">{num}.</span>
                    <span style="font-weight: 600; font-size: 16px; color: #2c3e50;">{criteria_name}</span>
                </div>
                <div style="display: flex; align-items: center; gap: 12px;">
                    <span style="background: {score_badge_color}; color: white; padding: 4px 12px; border-radius: 20px; font-size: 13px; font-weight: 600;">{score}/100 • {score_label}</span>
                    <span class="toggle-arrow" style="font-size: 14px; color: #7f8c8d;">▼</span>
                </div>
            </div>
            
            <!-- Card Content - Collapsible -->
            <div class="criterion-content" style="padding: 0 20px 20px 20px; display: block;">
        '''
        
        # Positive Features
        if data.get('positives'):
            html += '''
                <div style="background: #d4edda; border-radius: 10px; padding: 16px; margin-top: 16px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                        <span style="font-size: 18px;">✅</span>
                        <strong style="color: #155724; font-size: 15px;">Positive Features</strong>
                    </div>
                    <ul style="margin: 0; padding-left: 20px;">
            '''
            for positive in data['positives']:
                html += f'<li style="margin: 8px 0; color: #155724; line-height: 1.5;">{positive}</li>\n'
            html += '''
                    </ul>
                </div>
            '''
        
        # Omissions / Areas for Improvement
        if data.get('omissions'):
            html += '''
                <div style="background: #f8d7da; border-radius: 10px; padding: 16px; margin-top: 16px;">
                    <div style="display: flex; align-items: center; gap: 8px; margin-bottom: 12px;">
                        <span style="font-size: 18px;">⚠️</span>
                        <strong style="color: #721c24; font-size: 15px;">Omissions / Areas for Improvement</strong>
                    </div>
                    <ul style="margin: 0; padding-left: 20px;">
            '''
            for omission in data['omissions']:
                html += f'<li style="margin: 8px 0; color: #721c24; line-height: 1.5;">{omission}</li>\n'
            html += '''
                    </ul>
                </div>
            '''
        
        # Guideline Reference
        if data.get('guideline_ref'):
            html += f'''
                <div style="background: #e8f4f8; border-radius: 10px; padding: 12px 16px; margin-top: 16px;">
                    <div style="display: flex; align-items: center; gap: 8px;">
                        <span>📚</span>
                        <span style="color: #0b3c5d; font-size: 13px;"><strong>Guideline Reference:</strong> {data['guideline_ref']}</span>
                    </div>
                </div>
            '''
        
        html += '''
            </div>
        </div>
        '''
        
        return html
    
    def generate_full_report(self) -> str:
        """Generate complete standalone HTML report for download"""
        overall_score = self.results.get('overall_score', 0)
        score_color = self._get_score_color(overall_score)
        score_grade = self._get_grade(overall_score)
        
        html = f'''<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Article Critique Report - {self.filename}</title>
    <style>
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: -apple-system, BlinkMacSystemFont, 'Segoe UI', Roboto, 'Helvetica Neue', Arial, sans-serif;
            background: #f0f2f5;
            padding: 40px 20px;
            line-height: 1.6;
        }}
        
        .report-container {{
            max-width: 1000px;
            margin: 0 auto;
            background: white;
            border-radius: 20px;
            box-shadow: 0 20px 40px rgba(0,0,0,0.1);
            overflow: hidden;
        }}
        
        .report-header {{
            background: linear-gradient(135deg, #0b3c5d 0%, #1a4a6f 100%);
            color: white;
            padding: 48px;
            text-align: center;
        }}
        
        .report-header h1 {{
            font-size: 32px;
            margin-bottom: 12px;
            font-weight: 600;
        }}
        
        .report-header .filename {{
            opacity: 0.9;
            font-size: 14px;
            margin-top: 8px;
        }}
        
        .score-summary {{
            display: flex;
            justify-content: space-around;
            padding: 32px;
            background: #f8f9fa;
            border-bottom: 1px solid #e0e0e0;
            flex-wrap: wrap;
            gap: 20px;
        }}
        
        .score-card {{
            text-align: center;
            flex: 1;
            min-width: 180px;
        }}
        
        .score-number {{
            font-size: 48px;
            font-weight: bold;
            color: {score_color};
        }}
        
        .grade {{
            font-size: 28px;
            font-weight: bold;
            color: {score_color};
        }}
        
        .score-label {{
            color: #7f8c8d;
            margin-top: 8px;
            font-size: 14px;
        }}
        
        .criteria-section {{
            padding: 32px;
            border-bottom: 1px solid #e0e0e0;
        }}
        
        .criteria-header {{
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 20px;
            flex-wrap: wrap;
            gap: 10px;
        }}
        
        .criteria-title {{
            font-size: 20px;
            font-weight: bold;
            color: #2c3e50;
        }}
        
        .criteria-score {{
            font-size: 16px;
            font-weight: bold;
            padding: 6px 16px;
            border-radius: 30px;
            background: #f0f0f0;
        }}
        
        .positives, .omissions {{
            margin: 16px 0;
            padding: 20px;
            border-radius: 12px;
        }}
        
        .positives {{
            background: #d4edda;
            border-left: 4px solid #28a745;
        }}
        
        .omissions {{
            background: #f8d7da;
            border-left: 4px solid #dc3545;
        }}
        
        .positives h4, .omissions h4 {{
            margin-bottom: 12px;
            color: #333;
            font-size: 16px;
        }}
        
        .positives ul, .omissions ul {{
            margin-left: 24px;
        }}
        
        .positives li {{
            color: #155724;
            margin: 8px 0;
        }}
        
        .omissions li {{
            color: #721c24;
            margin: 8px 0;
        }}
        
        .guideline-ref {{
            margin-top: 16px;
            padding: 12px;
            background: #e8f4f8;
            border-radius: 8px;
            font-size: 13px;
            color: #0b3c5d;
        }}
        
        .report-footer {{
            background: #f8f9fa;
            padding: 24px;
            text-align: center;
            color: #7f8c8d;
            font-size: 13px;
        }}
        
        .recommendation-box {{
            background: #fff3cd;
            border-left: 4px solid #ffc107;
            border-radius: 12px;
            padding: 20px;
            margin: 20px 32px;
        }}
        
        @media (max-width: 768px) {{
            .score-summary {{
                flex-direction: column;
            }}
            .criteria-header {{
                flex-direction: column;
                align-items: flex-start;
            }}
            .report-header {{
                padding: 32px 20px;
            }}
            .criteria-section {{
                padding: 20px;
            }}
        }}
        
        .clearfix {{
            clear: both;
        }}
        
        hr {{
            margin: 20px 0;
            border: none;
            border-top: 1px solid #e0e0e0;
        }}
    </style>
</head>
<body>
    <div class="report-container">
        <div class="report-header">
            <h1>📋 Journal Article Critique Report</h1>
            <p class="filename">Analyzed: {self.filename}</p>
            <p class="filename">Generated: {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}</p>
        </div>
        
        <div class="score-summary">
            <div class="score-card">
                <div class="score-number">{overall_score}/100</div>
                <div class="score-label">Overall Scientific Quality Score</div>
            </div>
            <div class="score-card">
                <div class="grade">{score_grade}</div>
                <div class="score-label">Quality Grade</div>
            </div>
            <div class="score-card">
                <div class="score-number">{self._count_positives()}</div>
                <div class="score-label">Positive Findings</div>
            </div>
            <div class="score-card">
                <div class="score-number">{self._count_omissions()}</div>
                <div class="score-label">Areas for Improvement</div>
            </div>
        </div>
        
        <div class="recommendation-box">
            <strong>📌 Executive Summary:</strong> {self._generate_executive_summary()}
        </div>
'''
        
        # Generate each criterion section
        for i in range(1, 14):
            criterion_key = f'criterion_{i}'
            if criterion_key in self.results:
                html += self._generate_download_criterion_section(i, self.results[criterion_key])
        
        html += f'''
        <div class="report-footer">
            <p>Critique performed using CASP, STROBE, CONSORT, PRISMA, and SMART reporting guidelines.</p>
            <p>This assessment is for academic and research integrity purposes.</p>
            <p>🔗 <a href="https://wawerujm.github.io" target="_blank" style="color: #3498db; text-decoration: none;">wawerujm.github.io</a> | Evidence-Based Research Platform</p>
        </div>
    </div>
</body>
</html>
'''
        return html
    
    def _generate_download_criterion_section(self, num: int, data: Dict) -> str:
        """Generate HTML for a single criterion in download version"""
        score = data.get('score', 0)
        score_color = self._get_score_color(score)
        criteria_name = self.criteria_names.get(f'criterion_{num}', f'Criterion {num}')
        
        html = f'''
        <div class="criteria-section">
            <div class="criteria-header">
                <div class="criteria-title">{num}. {criteria_name}</div>
                <div class="criteria-score" style="background: {score_color}20; color: {score_color};">Score: {score}/100</div>
            </div>
'''
        
        if data.get('positives'):
            html += '''
            <div class="positives">
                <h4>✅ Positive Features</h4>
                <ul>
'''
            for positive in data['positives']:
                html += f'<li>{positive}</li>\n'
            html += '''
                </ul>
            </div>
'''
        
        if data.get('omissions'):
            html += '''
            <div class="omissions">
                <h4>⚠️ Omissions / Areas for Improvement</h4>
                <ul>
'''
            for omission in data['omissions']:
                html += f'<li>{omission}</li>\n'
            html += '''
                </ul>
            </div>
'''
        
        if data.get('guideline_ref'):
            html += f'''
            <div class="guideline-ref">
                📚 <strong>Reporting Guideline Reference:</strong> {data['guideline_ref']}
            </div>
'''
        
        html += '''
        </div>
'''
        return html
    
    def generate_markdown_report(self) -> str:
        """Generate markdown version of report"""
        overall_score = self.results.get('overall_score', 0)
        
        md = f"""# 📋 Journal Article Critique Report

**File:** {self.filename}
**Date:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Overall Score:** {overall_score}/100
**Grade:** {self._get_grade(overall_score)}

---

## Executive Summary

{self._generate_executive_summary()}

---

## Detailed Assessment

"""
        for i in range(1, 14):
            criterion_key = f'criterion_{i}'
            if criterion_key in self.results:
                data = self.results[criterion_key]
                md += f"### {i}. {self.criteria_names[criterion_key]}\n\n"
                md += f"**Score:** {data.get('score', 0)}/100\n\n"
                
                if data.get('positives'):
                    md += "#### ✅ Positive Features\n"
                    for p in data['positives']:
                        md += f"- {p}\n"
                    md += "\n"
                
                if data.get('omissions'):
                    md += "#### ⚠️ Omissions / Areas for Improvement\n"
                    for o in data['omissions']:
                        md += f"- {o}\n"
                    md += "\n"
                
                if data.get('guideline_ref'):
                    md += f"**Guideline Reference:** {data['guideline_ref']}\n\n"
                
                md += "---\n\n"
        
        md += f"\n*Report generated by Article Critique Platform | CASP | STROBE | CONSORT | PRISMA | SMART*\n"
        md += f"\n🔗 [wawerujm.github.io](https://wawerujm.github.io)\n"
        return md
    
    def _get_score_color(self, score: int) -> str:
        """Return color based on score"""
        if score >= 80:
            return "#28a745"
        elif score >= 60:
            return "#ffc107"
        elif score >= 40:
            return "#fd7e14"
        else:
            return "#dc3545"
    
    def _get_grade(self, score: int) -> str:
        """Return letter grade"""
        if score >= 90:
            return "A+ (Excellent)"
        elif score >= 80:
            return "A (Very Good)"
        elif score >= 70:
            return "B (Good)"
        elif score >= 60:
            return "C (Satisfactory)"
        elif score >= 50:
            return "D (Needs Improvement)"
        else:
            return "F (Poor Quality)"
    
    def _count_positives(self) -> int:
        """Count total positive findings"""
        count = 0
        for i in range(1, 14):
            key = f'criterion_{i}'
            if key in self.results:
                count += len(self.results[key].get('positives', []))
        return count
    
    def _count_omissions(self) -> int:
        """Count total omissions"""
        count = 0
        for i in range(1, 14):
            key = f'criterion_{i}'
            if key in self.results:
                count += len(self.results[key].get('omissions', []))
        return count
    
    def _generate_executive_summary(self) -> str:
        """Generate executive summary text"""
        overall = self.results.get('overall_score', 0)
        
        if overall >= 80:
            return "This article demonstrates ⭐ **high scientific rigor** with most quality criteria satisfied. The methodology is sound, reporting is transparent, and conclusions are justified. Minor improvements in specific areas would further strengthen the work."
        elif overall >= 60:
            return "This article shows 📊 **adequate scientific quality** but has notable gaps. While core elements are present, attention to reporting guidelines and addressing limitations would improve credibility. Consider revising based on identified omissions."
        elif overall >= 40:
            return "This article has ⚠️ **significant methodological or reporting deficiencies**. Critical appraisal reveals important gaps that may affect validity. Authors should address major omissions before considering this as high-quality evidence."
        else:
            return "This article has ❌ **major scientific quality concerns**. Substantial revisions are needed across multiple criteria. Consider seeking methodological support or following reporting guidelines more strictly."