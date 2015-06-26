using System;
using System.Globalization;
using System.IO;
using System.Linq;
using System.Xml.Linq;
using System.Collections.Generic;
using System.Xml;
using System.Text;

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
            String masterPath = "C:\\Users\\jortiz16\\Desktop\\";

            //query file
            StreamReader queryFile = new StreamReader(masterPath + "timesTPCH12.txt");

            //xml files on metrics
            List<String> xmlMetrics = new List<String>() { "cpu_user-12w-node001.xml", "mem_buffers-12w-node001.xml", "mem_cached-12w-node001.xml" };

            //query output
            StreamWriter queryMaxMetricsOut = new StreamWriter(masterPath + "outputTPCH12.txt");

            String currentLine = String.Empty;

            while ((currentLine = queryFile.ReadLine()) != null)
            {
                double queryStartEpoch = double.Parse(currentLine.Split(',')[2]);
                double queryEndEpoch = double.Parse(currentLine.Split(',')[3]);

                queryMaxMetricsOut.Write((int.Parse(currentLine.Split(',')[0]) + 1) + "," + double.Parse(currentLine.Split(',')[1]) + ",");
                Console.Write((int.Parse(currentLine.Split(',')[0]) + 1) + "," + double.Parse(currentLine.Split(',')[1]) + ",");
                foreach (String m in xmlMetrics)
                {
                    double maxValue = XmlRead(masterPath + m, queryStartEpoch, queryEndEpoch);
                    queryMaxMetricsOut.Write(maxValue + ",");
                    Console.Write(maxValue + ",");
                }
                queryMaxMetricsOut.Write("\n");
                Console.Write("\n");
            }
        }
        public double XmlRead(String metric_fileName, double startTime, double endTime)
        {
            double currentMetricMax = 0;
            int countLine = 0;
            using (TextReader textReader = new StreamReader(metric_fileName))
            {
                while (textReader.ReadLine() != null)
                {

                    StringBuilder rrd = new StringBuilder();
                    var line = textReader.ReadLine();
                    Boolean flagIrrelaventChunk = false;
                    if (line == "<rrd>")
                    {
                        rrd.Append(line);
                        do
                        {
                            countLine++;
                            if (line.Contains("<step>") && line.Contains("30"))
                            {
                                flagIrrelaventChunk = true;
                                break;
                            }
                            line = textReader.ReadLine();
                            rrd.Append(line);
                        }
                        while (line != "</rrd>");
                        if (!flagIrrelaventChunk)
                        {

                            double currentMetricValue = ProcessChunk(rrd.ToString(), startTime, endTime);
                            if (currentMetricValue > currentMetricMax)
                            {
                                currentMetricMax = currentMetricValue;
                            }
                        }


                    }
                }
            }
            return currentMetricMax;
        }

        private double ProcessChunk(string chunk, double startTime, double endTime)
        {
            double currentMetricMax = 0;
            XmlReaderSettings settings = new XmlReaderSettings();
            settings.ProhibitDtd = false;
            using (var metric_xmlFile_reader = XmlReader.Create(new StringReader(chunk), settings))
            {
                Boolean readMetricValue = false;
                while (metric_xmlFile_reader.Read())
                {
                    switch (metric_xmlFile_reader.NodeType)
                    {

                        case XmlNodeType.Text:
                            String metric_value = metric_xmlFile_reader.Value;
                            if (readMetricValue)
                            {
                                double currentMetricValue = Double.Parse(metric_value, NumberStyles.AllowExponent | NumberStyles.AllowDecimalPoint);
                                if (currentMetricValue > currentMetricMax)
                                {
                                    currentMetricMax = currentMetricValue;
                                }
                                readMetricValue = false; //unless proven otherwise later
                            }
                            break;
                        case XmlNodeType.Comment:
                            String comment = metric_xmlFile_reader.Value;
                            //try to parse the comment
                            try
                            {
                                int currentTime = Convert.ToInt32(comment.Substring(comment.IndexOf('/') + 1));
                                if (currentTime >= startTime && currentTime <= endTime)
                                {
                                    readMetricValue = true;
                                }

                            }
                            catch (Exception e)
                            {
                                //not a time format
                            }
                            break;

                    }
                }
            }
            return currentMetricMax;
        }

    }

}