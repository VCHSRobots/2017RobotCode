using System;
using System.Collections.Generic;
using System.Linq;
using System.Text;
using System.Threading.Tasks;

namespace MqttShow
{
    class StopWatch
    {

        [System.Runtime.InteropServices.DllImport("Kernel32.dll")]
        public static extern bool QueryPerformanceCounter(out long perfcount);

        [System.Runtime.InteropServices.DllImport("Kernel32.dll")]
        public static extern bool QueryPerformanceFrequency(out long freq);

        #region Query Performance Counter
        /// <summary>
        /// Gets the current 'Ticks' on the performance counter
        /// </summary>
        /// <returns>Long indicating the number of ticks on the performance counter</returns>
        public static long QueryPerformanceCounter()
        {
            long perfcount;
            QueryPerformanceCounter(out perfcount);
            return perfcount;
        }
        #endregion

        #region Query Performance Frequency
        /// <summary>
        /// Gets the number of performance counter ticks that occur every second
        /// </summary>
        /// <returns>The number of performance counter ticks that occur every second</returns>
        public static long QueryPerformanceFrequency()
        {
            long freq;
            QueryPerformanceFrequency(out freq);
            return freq;
        }
        #endregion

        #region Start()
        /// <summary>
        /// Returns a timestamp that can be used with Stop() to time the delay between calls.
        /// </summary>
        /// <returns></returns>
        public static long Start()
        {
            return QueryPerformanceCounter();
        }
        #endregion

        #region Stop()
        /// <summary>
        /// Returns the number of seconds that has elapsed since the coorisponding call to Start()
        /// </summary>
        /// <param name="timestamp">The returned value from a call to Start().</param>
        /// <returns></returns>
        public static double Stop(long timestamp)
        {
            long elapsedCount = QueryPerformanceCounter() - timestamp;
            double elapsedSeconds = (double)elapsedCount / (double) QueryPerformanceFrequency();
            return elapsedSeconds;
        }
        #endregion
    }
}
