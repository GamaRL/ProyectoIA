public interface IClusteringService
{
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  string GetCorrelationUrl(CorrelationAnalysisResponse response);
}