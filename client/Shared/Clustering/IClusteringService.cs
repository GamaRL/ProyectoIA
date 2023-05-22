public interface IClusteringService
{
  Task<CorrelationAnalysisResponse> GetCorrelationAnalysis(int fileId, bool containsHeaders);
  Task<List<ClusterResponse>> GetAgglomerativeClusters(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric, int noClusters, bool download = false);
  Task<List<ClusterResponse>> GetPartitionalClusters(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric, int noClusters, bool download = false);
  Task<string> GetAgglomarativeClustersImg(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric);
  Task<string> GetPartitionalClustersImg(int fileId, bool containsHeaders, List<object> columns, StandarizationMethod standarization, DistanceMetric metric);
  string GetImageUrl(string resource);
}