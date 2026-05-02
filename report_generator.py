"""
Generate HTML quality control report from FASTQ analysis
"""

def generate_html_report(fastq_file, output_html="quality_report.html"):
    """
    Generate comprehensive HTML QC report.
    
    Creates a professional report showing:
    - Overall quality statistics
    - Per-base quality plot
    - Quality distribution plot
    - Read length distribution plot
    - Bad cycles detection
    - Quality assessment & recommendations
    
    Args:
        fastq_file: Path to FASTQ file
        output_html: Output HTML filename
    """
    
    # Import needed functions
    from quality_calculator import (
        get_overall_stats,
        calculate_per_base_quality,
        detect_bad_cycles
    )
    from visualize import (
        plot_quality_profile,
        plot_quality_distribution,
        plot_read_length_distribution
    )
    
    print("Generating report...")
    
    # Get all statistics
    stats = get_overall_stats(fastq_file)
    avg_qual = calculate_per_base_quality(fastq_file)
    bad_cycles = detect_bad_cycles(avg_qual, threshold=20)
    
    # Generate plots
    print("  Creating visualizations...")
    plot_quality_profile(avg_qual)
    plot_quality_distribution(fastq_file)
    plot_read_length_distribution(fastq_file)
    
    # Determine quality rating
    if stats['average_quality'] >= 30:
        quality_rating = "EXCELLENT ✓"
        quality_color = "#48bb78"  # Green
        quality_description = "Data is high quality. Ready for downstream analysis."
    elif stats['average_quality'] >= 20:
        quality_rating = "GOOD ✓"
        quality_color = "#ed8936"  # Orange
        quality_description = "Data is acceptable. Mild trimming recommended."
    else:
        quality_rating = "POOR ✗"
        quality_color = "#e53e3e"  # Red
        quality_description = "Data quality is low. Recommend heavy trimming or resequencing."
    
    # Determine recommendations
    recommendations = []
    
    if len(bad_cycles) > 0:
        recommendations.append(f"⚠️ {len(bad_cycles)} bad cycles detected (Q < 20). Consider trimming end of reads.")
    else:
        recommendations.append("✓ No bad cycles detected. Quality is consistent across read length.")
    
    if stats['average_quality'] < 20:
        recommendations.append("⚠️ Overall quality is low. Consider resequencing.")
    elif stats['average_quality'] < 30:
        recommendations.append("⚠️ Trim low-quality bases (Q < 20) before alignment.")
    else:
        recommendations.append("✓ Quality is excellent. Ready for alignment without trimming.")
    
    if stats['average_read_length'] < 50:
        recommendations.append("⚠️ Read length is short. Check for adapter contamination.")
    else:
        recommendations.append("✓ Read length is appropriate for your analysis.")
    
    # Generate HTML
    html_content = f"""
    <!DOCTYPE html>
    <html lang="en">
    <head>
        <meta charset="UTF-8">
        <meta name="viewport" content="width=device-width, initial-scale=1.0">
        <title>FASTQ Quality Report</title>
        <style>
            * {{
                margin: 0;
                padding: 0;
                box-sizing: border-box;
            }}
            
            body {{
                font-family: 'Segoe UI', Tahoma, Geneva, Verdana, sans-serif;
                line-height: 1.6;
                color: #2d3748;
                background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
                padding: 20px;
            }}
            
            .container {{
                max-width: 1000px;
                margin: 0 auto;
                background: white;
                border-radius: 12px;
                box-shadow: 0 20px 60px rgba(0,0,0,0.3);
                overflow: hidden;
            }}
            
            .header {{
                background: linear-gradient(135deg, #1a365d 0%, #2c5282 100%);
                color: white;
                padding: 40px;
                text-align: center;
            }}
            
            .header h1 {{
                font-size: 2.5em;
                margin-bottom: 10px;
            }}
            
            .header p {{
                font-size: 1.1em;
                opacity: 0.9;
            }}
            
            .content {{
                padding: 40px;
            }}
            
            .section {{
                margin-bottom: 40px;
            }}
            
            .section h2 {{
                color: #2c5282;
                font-size: 1.8em;
                margin-bottom: 20px;
                padding-bottom: 10px;
                border-bottom: 3px solid #667eea;
            }}
            
            .stats-grid {{
                display: grid;
                grid-template-columns: repeat(auto-fit, minmax(250px, 1fr));
                gap: 20px;
                margin-bottom: 30px;
            }}
            
            .stat-box {{
                background: #f7fafc;
                border-left: 4px solid #4299e1;
                padding: 20px;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            
            .stat-label {{
                font-size: 0.9em;
                color: #718096;
                text-transform: uppercase;
                font-weight: 600;
                margin-bottom: 8px;
            }}
            
            .stat-value {{
                font-size: 1.8em;
                color: #2d3748;
                font-weight: bold;
            }}
            
            .quality-rating {{
                background: {quality_color};
                color: white;
                padding: 20px;
                border-radius: 8px;
                text-align: center;
                font-size: 1.5em;
                font-weight: bold;
                margin: 20px 0;
            }}
            
            .plot-container {{
                margin: 30px 0;
                text-align: center;
            }}
            
            .plot-container img {{
                max-width: 100%;
                border-radius: 8px;
                box-shadow: 0 2px 8px rgba(0,0,0,0.1);
            }}
            
            .plot-title {{
                font-size: 1.3em;
                color: #2d3748;
                margin-bottom: 15px;
                font-weight: 600;
            }}
            
            .recommendations {{
                background: #fffaf0;
                border-left: 4px solid #ed8936;
                padding: 20px;
                border-radius: 8px;
                margin: 20px 0;
            }}
            
            .recommendations h3 {{
                color: #c05621;
                margin-bottom: 15px;
            }}
            
            .recommendations ul {{
                list-style: none;
                margin-left: 0;
            }}
            
            .recommendations li {{
                padding: 8px 0;
                font-size: 1em;
            }}
            
            .footer {{
                background: #f7fafc;
                padding: 20px;
                text-align: center;
                border-top: 1px solid #e2e8f0;
                color: #718096;
                font-size: 0.9em;
            }}
            
            table {{
                width: 100%;
                border-collapse: collapse;
                margin: 20px 0;
            }}
            
            th {{
                background: #2c5282;
                color: white;
                padding: 12px;
                text-align: left;
                font-weight: 600;
            }}
            
            td {{
                padding: 12px;
                border-bottom: 1px solid #e2e8f0;
            }}
            
            tr:nth-child(even) {{
                background: #f7fafc;
            }}
        </style>
    </head>
    <body>
        <div class="container">
            <div class="header">
                <h1>📊 FASTQ Quality Control Report</h1>
                <p>Comprehensive sequencing quality analysis</p>
            </div>
            
            <div class="content">
                <!-- Summary Statistics -->
                <div class="section">
                    <h2>Summary Statistics</h2>
                    
                    <div class="stats-grid">
                        <div class="stat-box">
                            <div class="stat-label">Total Reads</div>
                            <div class="stat-value">{stats['total_reads']:,}</div>
                        </div>
                        
                        <div class="stat-box">
                            <div class="stat-label">Total Bases</div>
                            <div class="stat-value">{stats['total_bases']:,}</div>
                        </div>
                        
                        <div class="stat-box">
                            <div class="stat-label">Average Quality</div>
                            <div class="stat-value">Q{stats['average_quality']:.1f}</div>
                        </div>
                        
                        <div class="stat-box">
                            <div class="stat-label">Average Read Length</div>
                            <div class="stat-value">{stats['average_read_length']:.0f} bp</div>
                        </div>
                    </div>
                    
                    <div class="quality-rating">
                        Quality Assessment: {quality_rating}
                    </div>
                    
                    <p style="margin-top: 15px; color: #4a5568;">
                        {quality_description}
                    </p>
                </div>
                
                <!-- Quality Plots -->
                <div class="section">
                    <h2>Quality Control Plots</h2>
                    
                    <div class="plot-container">
                        <div class="plot-title">Per-Base Quality Score Profile</div>
                        <img src="quality_profile.png" alt="Quality Profile">
                        <p style="color: #718096; margin-top: 10px; font-size: 0.9em;">
                            Shows average quality score at each position in the read. Higher is better. Should stay above Q20 (orange line).
                        </p>
                    </div>
                    
                    <div class="plot-container">
                        <div class="plot-title">Quality Score Distribution</div>
                        <img src="quality_distribution.png" alt="Quality Distribution">
                        <p style="color: #718096; margin-top: 10px; font-size: 0.9em;">
                            Histogram showing how many bases have each quality score. Most bases should be Q30+ (right side).
                        </p>
                    </div>
                    
                    <div class="plot-container">
                        <div class="plot-title">Read Length Distribution</div>
                        <img src="read_lengths.png" alt="Read Lengths">
                        <p style="color: #718096; margin-top: 10px; font-size: 0.9em;">
                            Distribution of read lengths. Should show a narrow peak if sequencing and trimming were uniform.
                        </p>
                    </div>
                </div>
                
                <!-- Bad Cycles Detection -->
                <div class="section">
                    <h2>Bad Cycles Detection</h2>
                    
                    {f'''
                    <div style="background: #fff5f5; border-left: 4px solid #e53e3e; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <strong style="color: #c53030;">⚠️ {len(bad_cycles)} bad cycles detected (Q < 20)</strong>
                        <p style="margin-top: 10px;">Positions with low quality:</p>
                        <ul style="margin-left: 20px; margin-top: 10px;">
                    ''' if bad_cycles else '''
                    <div style="background: #f0fff4; border-left: 4px solid #48bb78; padding: 20px; border-radius: 8px; margin: 20px 0;">
                        <strong style="color: #22543d;">✓ No bad cycles detected!</strong>
                        <p style="margin-top: 10px;">All positions maintain quality above Q20 threshold.</p>
                    '''}
                    
                    {f"".join([f"<li>Position {pos}: Q{qual:.1f}</li>" for pos, qual in bad_cycles[:20]]) if bad_cycles else ""}
                    
                    {'</ul></div>' if bad_cycles else '</div>'}
                </div>
                
                <!-- Recommendations -->
                <div class="section">
                    <h2>Recommendations</h2>
                    
                    <div class="recommendations">
                        <h3>Quality Assessment & Next Steps:</h3>
                        <ul>
                            {chr(10).join([f"<li>{rec}</li>" for rec in recommendations])}
                        </ul>
                    </div>
                </div>
                
                <!-- Quality Interpretation -->
                <div class="section">
                    <h2>Quality Score Interpretation</h2>
                    
                    <table>
                        <tr>
                            <th>Quality Score</th>
                            <th>Error Probability</th>
                            <th>Accuracy</th>
                            <th>Interpretation</th>
                        </tr>
                        <tr>
                            <td>Q10</td>
                            <td>1 in 10</td>
                            <td>90%</td>
                            <td>Poor - Avoid</td>
                        </tr>
                        <tr>
                            <td>Q20</td>
                            <td>1 in 100</td>
                            <td>99%</td>
                            <td>Acceptable - Minimum threshold</td>
                        </tr>
                        <tr>
                            <td>Q30</td>
                            <td>1 in 1,000</td>
                            <td>99.9%</td>
                            <td>Good - Standard target</td>
                        </tr>
                        <tr>
                            <td>Q40</td>
                            <td>1 in 10,000</td>
                            <td>99.99%</td>
                            <td>Excellent - Very high quality</td>
                        </tr>
                    </table>
                </div>
            </div>
            
            <div class="footer">
                <p>Report generated by FASTQC Clone | Faneesh Kumar</p>
                <p>Analysis of {stats['total_reads']:,} reads ({stats['total_bases']:,} bases) from {fastq_file}</p>
            </div>
        </div>
    </body>
    </html>
    """
    
    # Write HTML file
    with open(output_html, 'w') as f:
        f.write(html_content)
    
    print(f"✓ Report generated: {output_html}")
    print(f"  Open in browser to view results!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) < 2:
        print("Usage: python report_generator.py <fastq_file>")
        print("Example: python report_generator.py data/real_data.fastq.gz")
        sys.exit(1)
    
    fastq_file = sys.argv[1]
    generate_html_report(fastq_file)