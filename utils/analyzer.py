import re
from typing import Dict, List, Any
import math

class ArticleAnalyzer:
    def __init__(self, text: str, depth: str, guidelines: List[str]):
        self.text = text
        self.depth = depth
        self.guidelines = guidelines
        self.sections = self._identify_sections(text)
        
    def _identify_sections(self, text):
        """Identify major sections of the article"""
        sections = {
            'title': self._extract_section(text, r'(?i)(title|título|titre)'),
            'abstract': self._extract_section(text, r'(?i)(abstract|summary|resumen|résumé)'),
            'introduction': self._extract_section(text, r'(?i)(introduction|intro|background|introducción)'),
            'methods': self._extract_section(text, r'(?i)(methods|methodology|material(s| and methods)|patients and methods|métodos)'),
            'results': self._extract_section(text, r'(?i)(results|findings|resultados)'),
            'discussion': self._extract_section(text, r'(?i)(discussion|discusión)'),
            'conclusion': self._extract_section(text, r'(?i)(conclusion|conclusions|conclusión)'),
            'references': self._extract_section(text, r'(?i)(references|bibliography|referencias)')
        }
        return sections
    
    def _extract_section(self, text, pattern):
        """Extract a section using regex pattern"""
        match = re.search(pattern, text, re.IGNORECASE)
        if match:
            start = match.start()
            # Get next 8000 characters or until next major heading
            end = min(start + 8000, len(text))
            return text[start:end]
        return ""
    
    def analyze_all_criteria(self) -> Dict:
        """Run analysis on all 13 criteria"""
        results = {}
        
        # Criteria 1: Article title and topic relevance
        results['criterion_1'] = self._assess_topic_relevance()
        
        # Criteria 2: Article source and strength
        results['criterion_2'] = self._assess_source_strength()
        
        # Criteria 3: Clarity of research title (PICO)
        results['criterion_3'] = self._assess_pico_clarity()
        
        # Criteria 4: Authors and affiliations
        results['criterion_4'] = self._assess_authors()
        
        # Criteria 5: Abstract as authentic summary
        results['criterion_5'] = self._assess_abstract_quality()
        
        # Criteria 6: Introduction/background
        results['criterion_6'] = self._assess_introduction_quality()
        
        # Criteria 7: Methodology suitability
        results['criterion_7'] = self._assess_methodology()
        
        # Criteria 8: Results and validity
        results['criterion_8'] = self._assess_results_validity()
        
        # Criteria 9: Analysis of data
        results['criterion_9'] = self._assess_data_analysis()
        
        # Criteria 10: Discussion of results
        results['criterion_10'] = self._assess_discussion()
        
        # Criteria 11: Conclusions
        results['criterion_11'] = self._assess_conclusions()
        
        # Criteria 12: Impact of research
        results['criterion_12'] = self._assess_impact()
        
        # Criteria 13: References and appropriateness
        results['criterion_13'] = self._assess_references()
        
        # Calculate overall score
        results['overall_score'] = self._calculate_overall_score(results)
        
        return results
    
    def _assess_topic_relevance(self) -> Dict:
        """Criterion 1: Topic relevance assessment"""
        score = 0
        positives = []
        omissions = []
        
        # Check for current scientific interest keywords
        current_keywords = ['novel', 'emerging', 'recent', 'current', 'trend', 'breakthrough', 'innovation']
        found_keywords = [kw for kw in current_keywords if kw.lower() in self.text.lower()]
        
        if found_keywords:
            score += 40
            positives.append(f"Addresses current scientific interest (mentions: {', '.join(found_keywords[:3])})")
        else:
            omissions.append("No explicit indication of current scientific relevance")
        
        # Check for gap in literature
        gap_indicators = ['gap in knowledge', 'unanswered question', 'limited research', 'need for investigation', 'remains unknown']
        if any(indicator in self.text.lower() for indicator in gap_indicators):
            score += 30
            positives.append("Identifies knowledge gap that justifies the research")
        else:
            omissions.append("Research gap not clearly articulated")
        
        # Check previous studies discussion
        if 'previous studies' in self.text.lower() or 'prior research' in self.text.lower() or 'literature' in self.text.lower():
            score += 30
            positives.append("Contextualizes within existing literature")
        else:
            omissions.append("Limited reference to previous studies addressing the question")
        
        return {
            'score': score,
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'SMART objectives framework'
        }
    
    def _assess_source_strength(self) -> Dict:
        """Criterion 2: Source and journal strength"""
        score = 0
        positives = []
        omissions = []
        
        # Look for journal impact factor mention
        impact_pattern = r'impact factor[:\s]*([\d\.]+)'
        impact_match = re.search(impact_pattern, self.text.lower())
        if impact_match:
            impact = impact_match.group(1)
            score += 30
            positives.append(f"Journal impact factor identified: {impact}")
        else:
            omissions.append("Journal impact factor unknown")
        
        # Check for publisher type indicators
        if 'open access' in self.text.lower() or 'springer' in self.text.lower() or 'elsevier' in self.text.lower():
            score += 20
            positives.append("Publisher identified (academic/professional)")
        else:
            omissions.append("Publisher information unclear")
        
        # Check for commercial interest disclosure
        if 'conflict' in self.text.lower() or 'competing interests' in self.text.lower():
            score += 25
            positives.append("Conflict of interest disclosure present")
        else:
            omissions.append("No conflict of interest statement found")
        
        # Check for funding source
        if 'funding' in self.text.lower() or 'grant' in self.text.lower() or 'supported by' in self.text.lower():
            score += 25
            positives.append("Funding source acknowledged")
        else:
            omissions.append("Funding source not disclosed")
        
        return {
            'score': score,
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'ICMJE recommendations'
        }
    
    def _assess_pico_clarity(self) -> Dict:
        """Criterion 3: PICO clarity in title"""
        score = 0
        positives = []
        omissions = []
        
        title_text = self.sections.get('title', self.text[:500])
        
        # Population identification
        pop_indicators = ['patients', 'participants', 'subjects', 'population', 'cohort', 'individuals']
        if any(ind in title_text.lower() for ind in pop_indicators):
            score += 25
            positives.append("Population clearly specified in title")
        else:
            omissions.append("Population not explicitly stated in title")
        
        # Intervention identification
        int_indicators = ['treatment', 'intervention', 'therapy', 'drug', 'surgery', 'procedure', 'exposure']
        if any(ind in title_text.lower() for ind in int_indicators):
            score += 25
            positives.append("Intervention/exposure mentioned in title")
        else:
            omissions.append("Intervention not clearly identified in title")
        
        # Comparison
        comp_indicators = ['versus', 'vs', 'compared to', 'comparison', 'control']
        if any(ind in title_text.lower() for ind in comp_indicators):
            score += 25
            positives.append("Comparison group referenced in title")
        else:
            omissions.append("Comparison group not specified in title")
        
        # Outcome
        out_indicators = ['outcome', 'effect', 'impact', 'association', 'risk', 'incidence', 'mortality']
        if any(ind in title_text.lower() for ind in out_indicators):
            score += 25
            positives.append("Primary outcome indicated in title")
        else:
            omissions.append("Primary outcome not evident from title")
        
        # Study design check
        design_indicators = ['randomized', 'cohort', 'case-control', 'cross-sectional', 'systematic review', 'meta-analysis']
        if any(ind in title_text.lower() for ind in design_indicators):
            positives.append("Study design included in title (good practice)")
        else:
            omissions.append("Study design not specified in title (optional but recommended)")
        
        return {
            'score': score,
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'PICO framework, CONSORT/STROBE'
        }
    
    def _assess_authors(self) -> Dict:
        """Criterion 4: Authors and affiliations"""
        score = 0
        positives = []
        omissions = []
        
        # Look for author section
        if 'author' in self.text.lower() or 'affiliation' in self.text.lower():
            score += 30
            positives.append("Author information provided")
        else:
            omissions.append("Author details not found in extracted text")
        
        # Check for domain expertise
        expertise_indicators = ['department of', 'institute of', 'university', 'hospital', 'center for']
        if any(ind in self.text.lower() for ind in expertise_indicators):
            score += 20
            positives.append("Author affiliations suggest domain expertise")
        else:
            omissions.append("Author affiliations not clearly stated")
        
        # Conflict of interest declaration
        coi_patterns = ['conflict of interest', 'competing interest', 'disclosure', 'declare']
        if any(pattern in self.text.lower() for pattern in coi_patterns):
            score += 30
            positives.append("Conflict of interest declaration present")
        else:
            omissions.append("No explicit conflict of interest statement")
        
        # ORCID or professional IDs
        if 'orcid' in self.text.lower() or '0000-000' in self.text:
            score += 20
            positives.append("Author ORCID/IDs provided (enhances transparency)")
        else:
            omissions.append("Author identifiers not found")
        
        return {
            'score': score,
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'ICMJE authorship criteria'
        }
    
    def _assess_abstract_quality(self) -> Dict:
        """Criterion 5: Abstract quality and IMRAD structure"""
        score = 0
        positives = []
        omissions = []
        
        abstract = self.sections.get('abstract', '')
        
        # Check IMRAD components
        imrad_components = {
            'background': ['background', 'introduction', 'context'],
            'methods': ['method', 'design', 'setting', 'participants'],
            'results': ['result', 'finding', 'outcome', 'effect size'],
            'conclusion': ['conclusion', 'implication', 'interpretation']
        }
        
        components_found = 0
        for component, keywords in imrad_components.items():
            if any(kw in abstract.lower() for kw in keywords):
                components_found += 1
        
        score += components_found * 15
        positives.append(f"Abstract follows IMRAD structure ({components_found}/4 components identified)")
        
        if components_found < 3:
            omissions.append("Abstract lacks structured IMRAD format")
        
        # Check for numerical data
        numbers = re.findall(r'\b\d+(?:\.\d+)?\b', abstract)
        if len(numbers) > 3:
            score += 15
            positives.append("Abstract contains quantitative data")
        else:
            omissions.append("Abstract lacks specific numerical findings")
        
        # Check for consistency signal
        if 'p<' in abstract or 'p=' in abstract or 'confidence interval' in abstract.lower():
            score += 15
            positives.append("Statistical results presented in abstract")
        
        # Sample size mention
        if any(word in abstract.lower() for word in ['n=', 'sample size', 'participants', 'patients']):
            score += 15
            positives.append("Sample size reported in abstract")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'CONSORT/STROBE abstract guidelines'
        }
    
    def _assess_introduction_quality(self) -> Dict:
        """Criterion 6: Introduction and background"""
        score = 0
        positives = []
        omissions = []
        
        intro = self.sections.get('introduction', '')
        
        # Literature knowledge
        citation_pattern = r'\(\d{4}\)|\[\d+\]|et al\.'
        citations = re.findall(citation_pattern, intro)
        if len(citations) > 5:
            score += 30
            positives.append(f"Demonstrates sound literature knowledge ({len(citations)} citations in introduction)")
        elif len(citations) > 0:
            score += 15
            positives.append("Some literature cited in introduction")
        else:
            omissions.append("Insufficient citation of pertinent literature")
        
        # Problem statement clarity
        problem_indicators = ['problem', 'gap', 'unclear', 'unknown', 'controversy', 'debate']
        if any(ind in intro.lower() for ind in problem_indicators):
            score += 20
            positives.append("Clear problem statement or knowledge gap identified")
        else:
            omissions.append("Research problem not clearly articulated")
        
        # SMART objectives
        smart_indicators = {
            'specific': ['specifically', 'aim', 'objective', 'purpose'],
            'measurable': ['measure', 'assess', 'quantify', 'evaluate'],
            'achievable': ['feasible', 'within', 'scope'],
            'relevant': ['important', 'significant', 'clinical', 'public health'],
            'time-bound': ['during', 'period', 'between', 'over']
        }
        
        smart_score = 0
        for key, indicators in smart_indicators.items():
            if any(ind in intro.lower() for ind in indicators):
                smart_score += 1
        
        score += smart_score * 6
        if smart_score >= 4:
            positives.append("Research objectives follow SMART framework")
        else:
            omissions.append("Objectives lack SMART specificity (consider making more Specific, Measurable, Achievable, Relevant, Time-bound)")
        
        # Logical flow
        flow_indicators = ['however', 'therefore', 'thus', 'consequently', 'furthermore']
        if any(ind in intro.lower() for ind in flow_indicators):
            score += 15
            positives.append("Logical flow and systematic argumentation")
        else:
            omissions.append("Introduction lacks clear logical progression")
        
        # Research question clarity
        if '?' in intro or any(word in intro.lower() for word in ['whether', 'if', 'to determine', 'to investigate']):
            score += 15
            positives.append("Research question explicitly stated")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'SMART criteria, scientific writing standards'
        }
    
    def _assess_methodology(self) -> Dict:
        """Criterion 7: Methodology suitability"""
        score = 0
        positives = []
        omissions = []
        
        methods = self.sections.get('methods', '')
        
        # Study design appropriateness
        designs = {
            'randomized controlled trial': ['randomized', 'rct', 'random allocation', 'controlled trial'],
            'cohort': ['cohort', 'follow-up', 'longitudinal', 'prospective'],
            'case-control': ['case-control', 'case control', 'matched'],
            'cross-sectional': ['cross-sectional', 'cross sectional', 'prevalence'],
            'systematic review': ['systematic review', 'meta-analysis', 'prisma']
        }
        
        design_found = None
        for design_name, keywords in designs.items():
            if any(kw in methods.lower() for kw in keywords):
                design_found = design_name
                score += 25
                positives.append(f"Study design clearly specified: {design_name}")
                break
        
        if not design_found:
            omissions.append("Study design not explicitly stated in methods")
        
        # Sample population representation
        sample_indicators = ['sample size', 'inclusion criteria', 'exclusion criteria', 'recruitment', 'consecutive']
        sample_quality = sum(1 for ind in sample_indicators if ind in methods.lower())
        score += sample_quality * 10
        if sample_quality >= 3:
            positives.append("Comprehensive sample description with inclusion/exclusion criteria")
        else:
            omissions.append("Sample population inadequately described")
        
        # Ethical considerations
        ethical_indicators = ['ethics', 'irb', 'institutional review board', 'informed consent', 'declaration of helsinki', 'ethical approval']
        if any(ind in methods.lower() for ind in ethical_indicators):
            score += 25
            positives.append("Ethical considerations properly addressed")
        else:
            omissions.append("No ethical approval or consent statement found (critical omission)")
        
        # Method reproducibility
        reproducibility = ['detailed', 'standard operating procedure', 'validated', 'protocol', 'registered']
        if any(ind in methods.lower() for ind in reproducibility):
            score += 15
            positives.append("Methods described with sufficient detail for reproducibility")
        else:
            omissions.append("Methods may lack detail for replication")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': design_found if design_found else 'CONSORT/STROBE/PRISMA'
        }
    
    def _assess_results_validity(self) -> Dict:
        """Criterion 8: Results and validity"""
        score = 0
        positives = []
        omissions = []
        
        results = self.sections.get('results', '')
        
        # Primary outcome statement
        if 'primary outcome' in results.lower() or 'primary endpoint' in results.lower():
            score += 25
            positives.append("Primary outcome variable clearly stated")
        else:
            omissions.append("Primary outcome not explicitly identified")
        
        # Secondary outcomes
        if 'secondary outcome' in results.lower() or 'secondary endpoint' in results.lower():
            score += 15
            positives.append("Secondary outcomes specified")
        
        # Validity and precision measures
        validity_indicators = ['confidence interval', 'ci', 'standard deviation', 'sd', 'standard error', 'se', 'range']
        if any(ind in results.lower() for ind in validity_indicators):
            score += 25
            positives.append("Measures of precision reported (CI/SD/SE)")
        else:
            omissions.append("No precision measures (CI/SD/SE) reported")
        
        # Error checking
        if 'p-value' in results.lower() or 'p =' in results.lower() or 'p<' in results.lower():
            score += 15
            positives.append("Statistical significance reported")
        
        # Presentation quality
        table_pattern = r'table\s+\d+'
        figure_pattern = r'figure\s+\d+'
        if re.search(table_pattern, results.lower()) or re.search(figure_pattern, results.lower()):
            score += 10
            positives.append("Data smartly presented with tables/figures")
        else:
            omissions.append("No tables or figures for data presentation")
        
        # Absence of errors (heuristic)
        if 'error' not in results.lower() and 'mistake' not in results.lower():
            score += 10
            positives.append("No obvious presentation errors detected")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'CONSORT/STROBE results reporting'
        }
    
    def _assess_data_analysis(self) -> Dict:
        """Criterion 9: Data analysis"""
        score = 0
        positives = []
        omissions = []
        
        methods = self.sections.get('methods', '')
        results = self.sections.get('results', '')
        analysis_text = methods + " " + results
        
        # Statistical software
        software = ['spss', 'sas', 'r statistic', 'stata', 'python', 'graphpad', 'prism', 'jmp', 'minitab']
        if any(sw in analysis_text.lower() for sw in software):
            score += 20
            positives.append("Statistical software/tools specified")
        else:
            omissions.append("Statistical computing tools not mentioned")
        
        # Data classification
        classification = ['categorical', 'continuous', 'ordinal', 'nominal', 'dichotomous', 'stratified', 'subgroup']
        if any(cls in analysis_text.lower() for cls in classification):
            score += 20
            positives.append("Data classification clearly described")
        else:
            omissions.append("Data classification not specified")
        
        # Summary statistics
        summary_stats = ['mean', 'median', 'mode', 'standard deviation', 'sd', 'variance', 'range', 'iqr', 'interquartile']
        if any(stat in analysis_text.lower() for stat in summary_stats):
            score += 20
            positives.append("Appropriate summary statistics presented")
        else:
            omissions.append("Summary statistics incomplete or missing")
        
        # Inferential statistics
        inferential = ['t-test', 'chi-square', 'anova', 'mann-whitney', 'wilcoxon', 'pearson', 'spearman', 'logistic regression', 'cox', 'kaplan-meier']
        if any(test in analysis_text.lower() for test in inferential):
            score += 25
            positives.append("Valid inferential statistical tests utilized")
        else:
            omissions.append("No inferential statistics or statitical models")
        
        # Assumption checks
        assumptions = ['normality', 'homogeneity', 'variance', 'assumption', 'kolmogorov-smirnov', 'shapiro-wilk', 'levene']
        if any(ass in analysis_text.lower() for ass in assumptions):
            score += 15
            positives.append("Statistical assumption checks reported")
        else:
            omissions.append("No verification of statistical assumptions")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'Statistical reporting guidelines'
        }
    
    def _assess_discussion(self) -> Dict:
        """Criterion 10: Discussion quality"""
        score = 0
        positives = []
        omissions = []
        
        discussion = self.sections.get('discussion', '')
        
        # Comparison with similar research
        comparison_indicators = ['consistent with', 'similar to', 'comparable to', 'in agreement with', 'corroborates']
        if any(ind in discussion.lower() for ind in comparison_indicators):
            score += 25
            positives.append("Balanced comparison with similar research")
        else:
            omissions.append("Lacks comparison with previous studies")
        
        # Contradictory evidence
        contradictory = ['however', 'contrary to', 'in contrast', 'different from', 'discrepancy', 'inconsistent']
        if any(ind in discussion.lower() for ind in contradictory):
            score += 20
            positives.append("Acknowledges contradictory or divergent findings")
        else:
            omissions.append("No discussion of contradictory evidence (possible bias)")
        
        # Limitations
        limitations = ['limitation', 'bias', 'confounding', 'generalizability', 'validity', 'weakness', 'constraint']
        if any(lim in discussion.lower() for lim in limitations):
            score += 30
            positives.append("Study limitations clearly outlined")
        else:
            omissions.append("No limitations section (essential for critical appraisal)")
        
        # Biased omissions/inclusions
        if 'selection bias' in discussion.lower() or 'publication bias' in discussion.lower():
            score += 15
            positives.append("Discusses potential bias in evidence synthesis")
        else:
            omissions.append("No discussion of bias in literature interpretation")
        
        # Clinical/real-world interpretation
        if 'clinical implication' in discussion.lower() or 'practice' in discussion.lower() or 'real world' in discussion.lower():
            score += 10
            positives.append("Translates findings to practical context")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'STROBE/CONSORT discussion section'
        }
    
    def _assess_conclusions(self) -> Dict:
        """Criterion 11: Conclusions justification and external validity"""
        score = 0
        positives = []
        omissions = []
        
        conclusion = self.sections.get('conclusion', '')
        results = self.sections.get('results', '')
        
        # Check if conclusion section exists
        if conclusion:
            # Justification by results
            if any(phrase in conclusion.lower() for phrase in ['showed', 'demonstrated', 'indicated', 'found that', 'revealed', 'suggest']):
                score += 35
                positives.append("Conclusion directly justified by study results")
            else:
                omissions.append("Conclusion may not be fully supported by results")
        else:
            omissions.append("Conclusion section unclear or missing")
            score += 10  # Partial credit for attempt to check
        
        # External validity / generalizability
        generalizability = ['general population', 'generalizable', 'external validity', 'real-world', 'broader population', 'generalizability']
        if any(gen in conclusion.lower() for gen in generalizability):
            score += 35
            positives.append("External validity/generalizability discussed")
        else:
            omissions.append("No discussion of applicability to general population")
        
        # Recommendation appropriateness
        if 'recommend' in conclusion.lower() or 'suggest' in conclusion.lower() or 'implication' in conclusion.lower():
            score += 15
            positives.append("Provides actionable recommendations")
        
        # Overstatement check
        overstatement_words = ['definitive', 'proves', 'conclusive', 'absolute']
        if any(word in conclusion.lower() for word in overstatement_words):
            omissions.append("Potential overstatement of conclusions (caution advised)")
        else:
            score += 15
            positives.append("Conclusions appropriately qualified")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'CONSORT/STROBE conclusion guidelines'
        }
    
    def _assess_impact(self) -> Dict:
        """Criterion 12: Impact of research results"""
        score = 0
        positives = []
        omissions = []
        
        full_text = self.text.lower()
        
        # Level of evidence assessment
        evidence_levels = {
            'Meta-analysis/Systematic Review': ['meta-analysis', 'systematic review', 'prisma'],
            'Randomized Controlled Trial': ['randomized controlled trial', 'rct', 'randomized'],
            'Cohort Study': ['cohort', 'prospective cohort', 'retrospective cohort'],
            'Case-Control Study': ['case-control', 'case control'],
            'Cross-sectional Study': ['cross-sectional', 'prevalence'],
            'Case Series/Report': ['case series', 'case report']
        }
        
        evidence_found = None
        for level, keywords in evidence_levels.items():
            if any(kw in full_text for kw in keywords):
                evidence_found = level
                if level in ['Meta-analysis/Systematic Review', 'Randomized Controlled Trial']:
                    score += 40
                    positives.append(f"High level of evidence: {level}")
                elif level in ['Cohort Study', 'Case-Control Study']:
                    score += 30
                    positives.append(f"Moderate level of evidence: {level}")
                else:
                    score += 20
                    positives.append(f"Lower level of evidence: {level}")
                break
        
        if not evidence_found:
            omissions.append("Level of evidence not clearly specified")
        
        # Practice changing impact
        impact_indicators = ['practice changing', 'clinical practice', 'guideline', 'recommendation', 'standard of care', 'change in practice']
        if any(ind in full_text for ind in impact_indicators):
            score += 30
            positives.append("Discusses practice-changing implications")
        else:
            omissions.append("No discussion of practice-changing impact")
        
        # Patient management impact
        patient_impact = ['patient management', 'patient care', 'treatment decision', 'clinical decision', 'patient outcome']
        if any(ind in full_text for ind in patient_impact):
            score += 30
            positives.append("Addresses impact on patient management")
        else:
            omissions.append("No clear statement on patient management implications")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'Oxford Centre for Evidence-Based Medicine Levels'
        }
    
    def _assess_references(self) -> Dict:
        """Criterion 13: References and appropriateness"""
        score = 0
        positives = []
        omissions = []
        
        references = self.sections.get('references', '')
        
        # Referencing style
        style_indicators = {
            'Vancouver': ['vancouver', 'superscript', '\\[\\d+\\]'],
            'Harvard': ['author-date', 'et al', '\\(\\w+, \\d{4}\\)'],
            'APA': ['apa', '\\w+ et al\\. \\(']
        }
        
        style_found = None
        for style, patterns in style_indicators.items():
            for pattern in patterns:
                if re.search(pattern, references, re.IGNORECASE):
                    style_found = style
                    score += 20
                    positives.append(f"Referencing style identified: {style}")
                    break
            if style_found:
                break
        
        if not style_found:
            omissions.append("Referencing style not clearly identifiable")
        
        # Currency of references (look for recent years)
        years = re.findall(r'\b(20[1-9][0-9]|202[0-5])\b', references)
        recent_years = [y for y in years if int(y) >= 2020]
        
        if len(recent_years) > 5:
            score += 30
            positives.append(f"Current references ({len(recent_years)} from 2020 onwards)")
        elif len(recent_years) > 0:
            score += 20
            positives.append(f"Some recent references ({len(recent_years)} from 2020 onwards)")
        else:
            omissions.append("References may be outdated (few from last 5 years)")
        
        # Bias assessment
        bias_indicators = ['english language', 'pubmed', 'medline', 'embase', 'cochrane']
        if any(ind in references.lower() for ind in bias_indicators):
            score += 25
            positives.append("Comprehensive database searching evident")
        else:
            omissions.append("Potential language or database bias not addressed")
        
        # Number of references
        ref_count = len(re.findall(r'\[\d+\]|\(\d{4}\)', references))
        if ref_count > 30:
            score += 15
            positives.append(f"Substantial reference list ({ref_count} citations)")
        elif ref_count > 10:
            score += 10
            positives.append(f"Adequate reference list ({ref_count} citations)")
        else:
            omissions.append(f"Limited reference list ({ref_count} citations) may indicate insufficient literature review")
        
        # Geographical bias check
        if 'china' in references.lower() or 'usa' in references.lower() or 'europe' in references.lower():
            score += 10
            positives.append("International literature referenced")
        
        return {
            'score': min(score, 100),
            'positives': positives,
            'omissions': omissions,
            'guideline_ref': 'Referencing standards (Vancouver/Harvard/APA)'
        }
    
    def _calculate_overall_score(self, results: Dict) -> int:
        """Calculate weighted overall score"""
        weights = {
            'criterion_1': 8,   # Topic relevance
            'criterion_2': 6,   # Source strength
            'criterion_3': 5,   # PICO clarity
            'criterion_4': 6,   # Authors
            'criterion_5': 7,   # Abstract
            'criterion_6': 8,   # Introduction
            'criterion_7': 10,  # Methodology (high weight)
            'criterion_8': 8,   # Results
            'criterion_9': 8,   # Data analysis
            'criterion_10': 8,  # Discussion
            'criterion_11': 7,  # Conclusions
            'criterion_12': 6,  # Impact
            'criterion_13': 5   # References
        }
        
        total_weighted_score = 0
        total_weight = 0
        
        for criterion, weight in weights.items():
            if criterion in results:
                score = results[criterion].get('score', 0)
                total_weighted_score += (score * weight)
                total_weight += weight
        
        if total_weight > 0:
            overall = total_weighted_score / total_weight
        else:
            overall = 0
        
        return int(round(overall))