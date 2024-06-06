from celery.result import AsyncResult
from rest_framework import status
from rest_framework.response import Response
from rest_framework.views import APIView
from .tasks import scrape_coin_data
from .serializers import CoinListSerializer, ScrapingStatusSerializer
from .models import ScrapedData
import uuid
from helpers.coin_mapping import COIN_MAP


class StartScrapingView(APIView):
    def post(self, request):
        serializer = CoinListSerializer(data=request.data)
        if serializer.is_valid():
            coins = serializer.validated_data['coins']
            # Generate a unique job id
            job_id = str(uuid.uuid4())
            for coin in coins:
                if coin.upper() in COIN_MAP.keys():
                    scrape_coin_data.apply_async(args=[coin, job_id], task_id=job_id)
            return Response({'job_id': job_id}, status=status.HTTP_200_OK)
        else:
            return Response(serializer.errors, status=status.HTTP_400_BAD_REQUEST)


class ScrapingStatusView(APIView):
    def get(self, request, job_id):
        # Check if the job with the given ID exists in Celery
        result = AsyncResult(job_id)
        if result.state == 'PENDING':
            # Job is still pending
            return Response({'status': 'pending'}, status=status.HTTP_200_OK)
        elif result.state == 'SUCCESS':
            # Job has completed successfully, retrieve scraped data
            scraped_data = ScrapedData.objects.filter(job_id=job_id)
            tasks = []
            for data in scraped_data:
                tasks.append({
                    'coin': data.coin_name,
                    'output': {
                        'price': data.price,
                        'price_change': data.price_change,
                        'market_cap': data.market_cap,
                        'market_cap_rank': data.market_cap_rank,
                        'volume': data.volume,
                        'volume_rank': data.volume_rank,
                        'volume_change': data.volume_change,
                        'circulating_supply': data.circulating_supply,
                        'total_supply': data.total_supply,
                        'diluted_market_cap': data.diluted_market_cap,
                        'contracts': data.contracts,
                        'official_links': data.official_links,
                        'socials': data.socials
                    }
                })
            response_data = {
                'job_id': job_id,
                'tasks': tasks
            }
            return Response(response_data, status=status.HTTP_200_OK)
        elif result.state == 'FAILURE':
            # Job has failed
            return Response({'error': 'Job failed'}, status=status.HTTP_500_INTERNAL_SERVER_ERROR)
        else:
            # Other states (e.g., RETRY, REVOKED)
            return Response({'status': result.state}, status=status.HTTP_200_OK)
