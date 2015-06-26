using System;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using System.Collections.Generic;

namespace gangliaQueryXMLMapper
{
	class gangliaXMLReader
	{
		public static void Main(string[] args)
		{
			gangliaXMLReader p = new gangliaXMLReader();
			p.readQueries();
		}
		public void readQueries()
		{
			String masterPath = "/Users/jortiz16/Documents/gangliaXMLData";

			//query file
			StreamReader queryFile = new StreamReader(masterPath + "timesTPCH12.txt");

			//xml files on metrics
			List<String> xmlMetrics = new List<String> () {"cpu_user-12w-node001.xml", "mem_buffers-12w-node001.xml", "mem_cached-12w-node001.xml"};

			//query output
			StreamWriter queryMaxMetricsOut = new StreamWriter (masterPath + "outputTPCH12.txt");

			String currentLine = String.Empty;

			while ((currentLine = queryFile.ReadLine()) != null)
			{
				double queryStartEpoch = double.Parse(currentLine.Split (',') [2]);
				double queryEndEpoch = double.Parse(currentLine.Split (',') [3]);

				queryMaxMetricsOut.Write((currentLine.Split(',')[0] + 1) + "," + double.Parse(currentLine.Split(',')[1]));
				foreach (String m in xmlMetrics) {
					double maxValue = readMetric (masterPath + m, queryStartEpoch, queryEndEpoch);
					Console.Write (maxValue + ",");
				}
				queryMaxMetricsOut.Write ("\n");
			}
		}

		public double readMetric(String metricFile, double startTime, double endTime)
		{
			double currentMetricMax = 0;
			foreach(var s in metricFile.Descendants("row")){
				var comment = s.PreviousNode as XComment;
				if (comment != null)
				{
					//Console.WriteLine(comment.Value);
					int currentTime = Convert.ToInt32(comment.Value.Substring(comment.Value.IndexOf('/')+1));

					//found the beginning
					if (currentTime >= startTime && currentTime <= endTime)
					{
						double currentMetricValue = Double.Parse(s.Value, NumberStyles.AllowExponent | NumberStyles.AllowDecimalPoint);
						if (currentMetricValue > currentMetricMax)
						{
							currentMetricMax = currentMetricValue;
						}
					}
				}
			} //end rows search

			return currentMetricMax;
		}
	}
}